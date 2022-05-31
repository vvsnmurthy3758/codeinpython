from tkinter import *

ws = Tk()
ws.title('PythonGuides')
ws.geometry('400x300')
ws.config(bg='#5F734C')

frame = Frame( ws,  bg='#A8B9BF')

text_box = Text(  frame,  height=13, width=32, font=(12) )
text_box.pack(side=LEFT,expand=True)
text_box.config(bg='#D9D8D7')

sb_ver = Scrollbar(  ws, orient=VERTICAL  )

sb_ver.pack(side=RIGHT, fill=Y)

text_box.config(yscrollcommand=sb_ver.set)
sb_ver.config(command=text_box.yview)


ws.mainloop()