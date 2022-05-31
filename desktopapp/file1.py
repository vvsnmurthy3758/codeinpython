from tkinter import *
from tkinter import ttk

ws = Tk()

ws.title('PythonGuides')
ws.geometry('500x500')

set = ttk.Treeview(ws)
set.pack()

set['columns'] = ('sno','plant name','size','quantity','rate','total price')
set.column('#0',width=0,stretch=False)
set.column("sno", anchor=CENTER, width=80,stretch=False)
set.column("plant name", anchor=CENTER, width=80,stretch=False)
set.column("size", anchor=CENTER, width=80,stretch=False)
set.column("quantity", anchor=CENTER, width=80,stretch=False)
set.column("rate", anchor=CENTER, width=80,stretch=False)
set.column("total price", anchor=CENTER, width=120,stretch=False)

set.heading("sno", text="S.NO", anchor=CENTER)
set.heading("plant name", text="Plant Name", anchor=CENTER)
set.heading("size", text="Size", anchor=CENTER)
set.heading("quantity", text="Quantity", anchor=CENTER)
set.heading("rate", text="Price per item", anchor=CENTER)
set.heading("total price", text="total price of item", anchor=CENTER)

# data
data = [
    [1, "mango", "15x16",200,150,30000],

]

global count
count = 0

for record in data:
    set.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2],record[3],record[4],record[5]))

    count += 1

Input_frame = Frame(ws)
Input_frame.pack()

id = Label(Input_frame, text="ID")
id.grid(row=0, column=0)

full_Name = Label(Input_frame, text="Full_Name")
full_Name.grid(row=0, column=1)

award = Label(Input_frame, text="Award")
award.grid(row=0, column=2)

id_entry = Entry(Input_frame)
id_entry.grid(row=1, column=0)

fullname_entry = Entry(Input_frame)
fullname_entry.grid(row=1, column=1)

award_entry = Entry(Input_frame)
award_entry.grid(row=1, column=2)


def input_record():
    global count

    set.insert(parent='', index='end', iid=count, text='',
               values=(id_entry.get(), fullname_entry.get(), award_entry.get()))
    count += 1

    id_entry.delete(0, END)
    fullname_entry.delete(0, END)
    award_entry.delete(0, END)


# button
Input_button = Button(ws, text="Input Record", command=input_record)

Input_button.pack()

ws.mainloop()

#https://pythonguides.com/python-tkinter-table-tutorial/#Python_Tkinter_Table_Input