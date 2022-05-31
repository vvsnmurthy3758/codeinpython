import os
from bold import builders, util
import sys
import logging
import argparse
import shelve
from bold import util
import inspect
import string
import hashlib
import errno


build_path = util.Lazy_build_path('{build_path}')


SHELVE_PICKLE_PROTOCOL = 2


log = logging.getLogger(__name__)


def _parse_args ():
	p = argparse.ArgumentParser()
	p.add_argument('--state-file', default = '.bold_state', help = "Bold internal state DB file name")
	p.add_argument('--build-path', default = 'build/dev/', help = "Target build directory path") #TODO build/dev->build
	p.add_argument('--reset', '-r', action = 'store_true', help = "Delete Bold state file")
	p.add_argument('--print-ood', action = 'store_true', help = "Print out-of-date files")
	return p.parse_known_args()[0]

def _init_logging ():
	# format = '%(asctime)s %(levelname)-5s [%(filename)s:%(funcName)s:%(lineno)d]  %(message)s'
	format = '%(levelname)-5s  %(message)s'
	logging.basicConfig(level = logging.DEBUG, format = format)

def run ():
	args = _parse_args()

	_init_logging()

	if args.reset:
		try:
			os.remove(args.state_file)
		except OSError as e:
			if e.errno != errno.ENOENT:
				raise

	module = util.load_user_module()

	db = shelve.open(args.state_file, protocol = SHELVE_PICKLE_PROTOCOL)
	try:
		util.create_dir_recursive(args.build_path)

		# detect class changes
		module_code = inspect.getsource(module)
		changed_classes = {}
		for builder_class in builders._registered_builders:
			cur_class_code = inspect.getsource(builder_class)
			#TODO ignore comments (use compile.parse?)
			cur_ccode_hash = hashlib.md5(''.join(filter(None, map(string.strip, cur_class_code.splitlines())))).digest()
			cl_hash_key = 'class_code_hash:' + repr(builder_class)
			if cur_ccode_hash != db.get(args.build_path + cl_hash_key):
				def save_hash (cl_hash_key=cl_hash_key, cur_ccode_hash=cur_ccode_hash):
					db[args.build_path + cl_hash_key] = cur_ccode_hash
				changed_classes[builder_class] = save_hash

			module_code = module_code.replace(cur_class_code, '')

		# detect other module changes
		cur_mlcode_hash = hashlib.md5(''.join(filter(None, map(string.strip, module_code.splitlines())))).digest()
		if cur_mlcode_hash != db.get(args.build_path + 'module_level_code_hash'):
			log.warning("Cannot analyze some of your build script changes,"
				" *maybe* you need to force rebuild something manually (or just everything with --reset if you are unsure)")
			db[args.build_path + 'module_level_code_hash'] = cur_mlcode_hash

		# process deps
		bs = []
		for builder_class in builders._registered_builders:
			b = builder_class(db, args.build_path, args.print_ood)

			if not (isinstance(b.sources, (basestring, list, tuple)) or callable(b.sources)):
				raise TypeError("builder %s has invalid .sources: %s" % (b, b.sources))

			if callable(b.sources):
				actual_src_paths = b.sources()
				assert actual_src_paths
			elif isinstance(b.sources, basestring):
				actual_src_paths = util.lazy_glob(b.sources)(None)
				assert actual_src_paths
			elif isinstance(b.sources, (list, tuple)):
				actual_src_paths = []
				for mask in b.sources:
					paths = util.lazy_glob(mask)(None)
					if not paths:
						raise ValueError("File mask produced empty result: %s" % mask)
					actual_src_paths += paths

			# saved_src_paths = []
			# new_paths = set(actual_src_paths) - set(saved_src_paths)
			# deleted_paths = set(saved_src_paths) - set(actual_src_paths)
			#TODO handle deleted_paths
			b.handle_dependencies(actual_src_paths)
			#+handle deps diff

			force_rebuild = builder_class in changed_classes
			changed_targets = b._process_deps(force_rebuild = force_rebuild)

			# if changed_targets:
			# 	logger.debug("Out of date targets: %s" % ', '.join(changed_targets))

			bs.append((b, changed_targets, actual_src_paths, force_rebuild))
			# print b._tmp_deps
			# print b._tmp_files

		# resolve order and build
		def cmp (b1, b2):
			b1 = b1[0]
			b2 = b2[0]

			for dp in b1._tmp_deps.keys():
				if (dp not in b1._tmp_files) and (dp in b2._tmp_files):
					# b2 requires b1
					return -1

			for dp in b2._tmp_deps.keys():
				if (dp not in b2._tmp_files) and (dp in b1._tmp_files):
					return 1

			return 0
		bss = sorted(bs, cmp=cmp)
		# print [i[0] for i in bss]
		for b, changed_targets, actual_src_paths, force_rebuild in bss:
			# print; print b
			if changed_targets:
				b.build(changed_targets, actual_src_paths)
				if force_rebuild:
					changed_classes[b.__class__]()
	finally:
		db.close()