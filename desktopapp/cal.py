from tkinter import *
from tkinter import ttk


def calculate(*args):
    try:
        value = float(feet.get())
        meters.set((0.3048 * value * 10000.0 + 0.5) / 10000.0)
    except ValueError:
        pass


root = Tk()
root.title("feet to meters")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, E, W, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
feet = StringVar()
meters = StringVar()

feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
feet_entry.grid(column=5, row=1)

ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2)
ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3)
ttk.Label(mainframe, text="feet").grid(column=3, row=1)
ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2)
ttk.Label(mainframe, text="meters").grid(column=3, row=2)
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
feet_entry.focus()
root.bind('<Return>', calculate)
root.mainloop()
