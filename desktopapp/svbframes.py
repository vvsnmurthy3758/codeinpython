# svbframes
import json
import subprocess
from tkinter import *
from tkinter import ttk
from ttkwidgets.autocomplete import AutocompleteCombobox
import self as self


class NewBill():
    pltnames = ['Terminelia', 'mahagani', 'kalapati sapota', 'nimmma', 'danimma', 'cycas',
                'chinnarasam', 'pedharasam', 'neelam', 'kesari', 'collector mamidi', 'cherukurasam']
    data = [('S.NO', 'Name of plant', 'Size of plant', 'Quantity', 'Price per item', 'Amount'), ]
    pltsizes = ['8x9', '9x11', '13x13', '15x15', '18x18', '21x21', '25x25', '30x30']
    pltno = 0
    m = 0

    customer_name=''
    customer_street=''
    customer_city=''
    customer_state=''

    def showdata(self):
        # for i in self.data:
        self.table.insert(parent='', index='end', iid=self.m, text='',
                          values=self.data[self.pltno])
        self.m += 1

    def resetentries(self):
        self.entry_pltname.delete(0, 'end')
        self.entry_pltsize.delete(0, 'end')
        self.entry_pltqty.delete(0, 'end')
        self.entry_pltprice.delete(0, 'end')
        self.entry_pltname.focus()

    def adddata(self, name, sz, qty, rate,cn,cas,cac,cast):
        tp = int(qty) * int(rate)
        print(name, sz, qty, rate, qty, tp)
        print('printed')
        self.pltno += 1
        self.data.append((self.pltno, name, sz, qty, rate, tp))
        print(self.data)
        self.customer_name=cn
        self.customer_street=cas
        self.customer_city=cac
        self.customer_state=cast

        self.showdata()
        self.entry_pltno.configure(text=self.pltno + 1)
        self.resetentries()

    def callback(self, event):
        self.labelframe["text"] = "You pressed {}".format(event.keysym)

    def __init__(self, master, m, n):
        self.master = master

        self.labelframe = LabelFrame(master, text="New Bill", bg='#B8F492', font=("times new roman", 15, "bold"), bd=8,
                                     relief=GROOVE)
        self.labelframe.grid(row=m, column=n, columnspan=8, sticky=(N, S, E, W))

        self.scroll = Scrollbar(self.labelframe)
        self.scroll.pack(side=RIGHT, fill=Y)

        self.entrys = Frame(self.labelframe, bg='#B8F492')
        self.entrys.pack()
        #add customer entry boxes
        self.custonernamelabel = Label(self.entrys, font=('Times', 14), text='customer name', width=15)
        self.custonernamelabel.grid(row=0,column=0)
        self.entry_customername = Entry(self.entrys, width=20, font=('Times', 14), )
        self.entry_customername.grid(row=0, column=1, padx=10, pady=5)
        self.custoneraddresslabel = Label(self.entrys, font=('Times', 14), text='address', width=5)
        self.custoneraddresslabel.grid(row=0,column=2)
        self.entry_customeraddress_street = Entry(self.entrys, width=20, font=('Times', 14), )
        self.entry_customeraddress_street.grid(row=0, column=3, padx=10, pady=5)
        self.entry_customeraddress_city = Entry(self.entrys, width=20, font=('Times', 14), )
        self.entry_customeraddress_city.grid(row=0, column=4, padx=10, pady=5)
        self.entry_customeraddress_state = Entry(self.entrys, width=20, font=('Times', 14), )
        self.entry_customeraddress_state.grid(row=0, column=5, padx=10, pady=5)
        #add plants entry boxes
        self.entry_pltno = Label(self.entrys, font=('Times', 14), text=self.pltno + 1, width=5)
        self.entry_pltno.grid(row=1, column=0, padx=10, pady=5)
        self.entry_pltname = AutocompleteCombobox(self.entrys, width=20, font=('Times', 14),
                                                  completevalues=self.pltnames)
        self.entry_pltname.grid(row=1, column=1, padx=10, pady=5)
        self.entry_pltsize = AutocompleteCombobox(self.entrys, width=20, font=('Times', 14),
                                                  completevalues=self.pltsizes)
        self.entry_pltsize.grid(row=1, column=2, padx=10, pady=5)
        self.entry_pltqty = Entry(self.entrys, width=20, font=('Times', 14), )
        self.entry_pltqty.grid(row=1, column=3, padx=10, pady=5)
        self.entry_pltprice = Entry(self.entrys, width=20, font=('Times', 14), )
        self.entry_pltprice.grid(row=1, column=4, padx=10, pady=5)
        #self.entry_totalprice = Entry(self.entrys, width=20, font=('Times', 14), )
        #self.entry_totalprice.grid(row=0, column=5, padx=10, pady=5)
        #self.entry_totalprice.insert(0, 'auto write')
        self.addbutton = Button(self.entrys, text='add', width=20, bg='blue', fg='white',
                                command=lambda: self.adddata(
                                    self.entry_pltname.get(),
                                    self.entry_pltsize.get(),
                                    self.entry_pltqty.get(),
                                    self.entry_pltprice.get(),
                                    self.entry_customername.get(),
                                    self.entry_customeraddress_street.get(),
                                    self.entry_customeraddress_city.get(),
                                    self.entry_customeraddress_state.get(),
                                ))
        self.addbutton.grid(row=1, column=5,)



        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 16)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders

        self.table = ttk.Treeview(self.labelframe, yscrollcommand=self.scroll.set,style="mystyle.Treeview")
        self.table.pack()

        self.table['columns'] = ['S.No', 'plant_name', 'plant_size', 'plant_quantity', 'plant_price', 'total_ price']

        self.table.column('#0', stretch=NO, anchor=CENTER, width=0)
        self.table.heading('#0', text='')
        self.table.config(height=25)

        for i in self.table['columns']:
            self.table.column(i, stretch=NO, anchor=CENTER)
            self.table.heading(i, text=i)
        self.addbutton.bind('<Return>',lambda x: self.adddata(
                                    self.entry_pltname.get(),
                                    self.entry_pltsize.get(),
                                    self.entry_pltqty.get(),
                                    self.entry_pltprice.get(),
                                    self.entry_customername.get(),
                                    self.entry_customeraddress_street.get(),
                                    self.entry_customeraddress_city.get(),
                                    self.entry_customeraddress_state.get(),
                                ))
        self.printbutton=Button(self.labelframe,text='print',command=self.addtojson)
        self.printbutton.pack()

    def printinvoice(self):
        print("in print invoice module")
        subprocess.call('printsystem.py',shell=True)


    def addtojson(self):
        print("started add to json method")
        with open('billdata.json', 'r+') as file:
            file_data = json.load(file)
            print("file_data",file_data[-1]['invoice number'])
            invoice_number=file_data[-1]['invoice number']
            jsondata={
                'invoice number':invoice_number+1,
                'cn':self.customer_name,
                'street':self.customer_street,
                'city':self.customer_city,
                'state':self.customer_state,
                'purchased':self.data
            }
            file_data.append(jsondata)
            file.seek(0)
            json.dump(file_data, file, indent=4)
        self.printinvoice()
        print("called print invoice")

class NewCustomer():
    def __init__(self, master, m, n):
        self.master = master

        self.labelframe = LabelFrame(master, text="Add Customer Page ", bg='#B8F492', font=("times new roman", 15, "bold"), bd=8,
                                     relief=GROOVE)
        self.labelframe.grid(row=m, column=n, columnspan=8)

        self.customer_name=Label(self.labelframe,text="Customer name")
        self.customer_name.grid(row=0,column=0,sticky=E)
        self.customer_name_entry = Entry(self.labelframe,width=20)
        self.customer_name_entry.grid(row=0,column=1)
        self.customer_name = Label(self.labelframe, text="Adress")
        self.customer_name.grid(row=1,column=0,sticky=E)
        self.customer_name_entry = Entry(self.labelframe,width=20)
        self.customer_name_entry.grid(row=0,column=1)
        self.customer_name = Label(self.labelframe, text="DoorNumber, Street")
        self.customer_name.grid(row=2,column=0,sticky=E)
        self.customer_name_entry = Entry(self.labelframe,width=20)
        self.customer_name_entry.grid(row=0,column=1)
        self.customer_name = Label(self.labelframe, text="City")
        self.customer_name.grid(row=3,column=0,sticky=E)
        self.customer_name_entry = Entry(self.labelframe,width=20)
        self.customer_name_entry.grid(row=0,column=1)
        self.customer_name = Label(self.labelframe, text="State")
        self.customer_name.grid(row=4,column=0,sticky=E)
        self.customer_name_entry = Entry(self.labelframe,width=20)
        self.customer_name_entry.grid(row=0,column=1)



class FetchBill():
    def __init__(self, master, m, n):
        self.master = master

        self.labelframe = LabelFrame(master, text="New Bill", bg='#B8F492', font=("times new roman", 15, "bold"), bd=8,
                                     relief=GROOVE)
        self.labelframe.grid(row=m, column=n, columnspan=8, sticky=(N, S, E, W))

class ViewCustomers():
    def __init__(self, master, m, n):
        self.master = master

        self.labelframe = LabelFrame(master, text="New Bill", bg='#B8F492', font=("times new roman", 15, "bold"), bd=8,
                                     relief=GROOVE)
        self.labelframe.grid(row=m, column=n, columnspan=8, sticky=(N, S, E, W))


#tasks
##add database

##add printer fuction
##add fetch bills
##add edit customer
##add import excel to table
