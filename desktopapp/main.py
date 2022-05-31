from tkinter import *
from tkinter import ttk
from tkinter.ttk import Notebook
from PIL import Image, ImageTk
from pyxll import xl_menu, create_ctp, CTPDockPositionFloating
import svbframes
import pyglet, tkinter
pyglet.font.add_file("C:\Windows\Fonts\COOPBL.TTF")


def exit():
    app.destroy()


def select(n):
    frame2.select(n)


app = Tk()
app.title("sri veerabhadra nursery & gardens")
width = app.winfo_screenwidth()
height = app.winfo_screenheight()
app.configure(width=width, height=height, bg='#71EDCB')
app.grid_propagate(False)
#app.resizable(False, False)
print(width)
print(height)

# logo and title
titleframe = Frame(master=app, width=width, height=80, bg='white')
titleframe.grid_propagate(False)
logo = Image.open("images/svblogo.png")
logo=logo.resize((100,80))
logo=ImageTk.PhotoImage(logo)
logolabel = Label(titleframe, image=logo, bg='white',)
com_title = Label(titleframe, text="Sri Veerabhadra Nursery & gardens", font=('Cooper Black', 25,),
                  bg='white', fg='black', padx=100, )
logoutlabel = Button(titleframe, text="logout",font=('Cooper', 10, 'bold'),command=exit)
logolabel.grid(column=0, row=0, padx=100)
titleframe.grid(row=0, column=0, columnspan=8)
com_title.grid(row=0, column=1, sticky=N)
logoutlabel.grid(row=0, column=3, sticky=E)
# -------------------------


# frame2-notebook
frame2 = Notebook(app,)

tab1 = Frame(frame2,bg='#B8F492')
frame2.add(tab1, text='tab1')

tab2 = Frame(frame2)
frame2.add(tab2, text='tab2', )
newcustomer = svbframes.NewCustomer(tab1, 0, 0)
newbill = svbframes.NewBill(tab2, 0, 0)

tab3 = Frame(frame2)
frame2.add(tab3, text='tab2', )
fetchbill = svbframes.FetchBill(tab3, 0, 0)

tab4 = Frame(frame2)
frame2.add(tab4, text='tab2', )
viewcustomers = svbframes.ViewCustomers(tab4, 0, 0)


frame2.grid(row=1, column=1, columnspan=7, sticky=(N, S, E, W))

# frame1
frame1 = Frame(master=app, width=width / 10, height=500, bg='#B8F492', bd=8, relief=GROOVE)
frame1.grid_propagate(False)
label1 = Button(frame1, text='New Bill', font=('Ariel', 18, 'bold'), bg='green', fg='white', relief=GROOVE,
                command=lambda: select(0))
label2 = Button(frame1, text='new Customer', font=('Ariel', 18, 'bold'), bg='green', fg='white', relief=GROOVE,
                command=lambda: select(1))
label3 = Button(frame1, text='fetch bill', font=('Ariel', 18, 'bold'), bg='green', fg='white', relief=GROOVE,
                command=lambda: select(2))
label4 = Button(frame1, text='view customers', font=('Ariel', 18, 'bold'), bg='green', fg='white', relief=GROOVE,
                command=lambda: select(3))

frame1.grid(column=0, row=1, sticky=(NW, N, S, E, W), padx=5)
label1.grid(row=0, column=0)
label2.grid(row=2, column=0)
label3.grid(row=3, column=0)
label4.grid(row=4, column=0)
# -----------------------------------------


app.mainloop()
#
