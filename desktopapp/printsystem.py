import json
import os
from datetime import date, datetime
from reportlab.lib.colors import HexColor
from reportlab.lib.units import cm, inch
from reportlab.pdfgen import canvas
# a4sheet size:3508 x 2480 px 21x29.7cm  vslues:600x790
from reportlab.platypus import Table, TableStyle
import svbframes

print('started print invoice')

pagewidth = 600
pageheight = 790
customer_name=''
customer_street=''
customer_city=''
customer_state=''
invoice_number=1
data=[]
total_bill=0
#import data from json
def loadjsondata():
    f=open('billdata.json')
    datajson=json.load(f)
    print("json loaded")
    print(datajson[-1])
    global customer_name
    global customer_street
    global customer_city
    global customer_state
    global invoice_number
    global data
    global total_bill
    invoice_number=datajson[-1]['invoice number']
    customer_name= datajson[-1]['cn']
    customer_street= datajson[-1]['street']
    customer_city= datajson[-1]['city']
    customer_state= datajson[-1]['state']
    data=datajson[-1]['purchased']
    print('customer_name',customer_name)
    for i in data:
        if type(i[5])== int or i[5].isdigit():
            total_bill+=i[5]
    print('loaded variables corectly')
    f.close()
loadjsondata()

# creating pdf
c = canvas.Canvas("firstfile.pdf")
c.setPageSize((pagewidth, pageheight))

# border
c.drawBoundary('outline border', 20, 15, pagewidth - 40, pageheight - 40)

# title
title = 'SRI VEERABHADRA NURSERY & GARDENS'
# default fonts
""""
'Courier', 'Courier-Bold', 'Courier-Oblique', 'Courier-BoldOblique',
    'Helvetica', 'Helvetica-Bold', 'Helvetica-Oblique', 'Helvetica-BoldOblique',
    'Times-Roman', 'Times-Bold', 'Times-Italic', 'Times-BoldItalic',
    'Symbol','ZapfDingbats'
"""
# newfont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Showg', 'SHOWG.TTF'))
pdfmetrics.registerFont(TTFont('Forte', 'FORTE.TTF'))
pdfmetrics.registerFont(TTFont('Cooper', 'COOPBL.TTF'))
pdfmetrics.registerFont(TTFont('Calibri', 'CALIBRI.TTF'))
# pdfmetrics.registerFont(TTFont('Cooperitalic', 'CooperOldstyleBQ-Italic.otf'))


c.setFont('Cooper', 22)
c.drawString(75, pageheight - 60, title)
# tagline
c.setFont('Forte', 8)
c.drawString(180, pageheight - 70, 'All varieties of fruits ,flowers and avenue plants are available')

# logo
c.drawImage('images/svblogo.png', 30, pageheight - 70, 40, 40)

# address
c.setFont('Calibri', 8)
c.drawString(35, pageheight - 80, 'K.Venkeswara Rao +91 9441026375')
c.drawString(35, pageheight - 90, 'V.V.S.N.Murthy K +91 8367226375')
c.drawString(35, pageheight - 100, 'NH-16,Burrilanka,Rajahmundry,')
c.drawString(35, pageheight - 110, 'EGDT,Andrapradesh-533126')
c.drawString(35, pageheight - 120, 'email:sriveerabhadranursery@gmail.com')
c.drawString(35, pageheight - 130, 'website:www.sriveerabhadranursery.com')

# invoice number
c.setFont('Calibri', 10)
c.drawString(450, pageheight - 110, 'Invoice Number: ' + str(invoice_number))

# Date
Date = date.today()
d = Date.strftime("%B %d, %Y")
c.drawString(450, pageheight - 120, 'Date: ' + d)

# time
import time

t = time.strftime("%I:%M %p")
c.drawString(450, pageheight - 130, 'Time: ' + t)

# Bill to
c.setFillColorRGB(0,0,0)
c.rect(25, pageheight - 161, 200, 12,stroke=0, fill=1)
c.setFillColorRGB(1,1,1)
c.drawString(30, pageheight - 159, 'Bill To:')
c.setFillColorRGB(0,0,0)

# customer name
c.drawString(25, pageheight - 175, 'Name:')
c.setFont('Cooper', 12)
c.drawString(65, pageheight - 175, customer_name)

# customer adress
c.setFont('Calibri', 10)
c.drawString(25, pageheight - 185, 'Address:')
customer_address_street = customer_street
customer_address_city= customer_city
customer_address_state = customer_state
c.drawString(65, pageheight - 185, customer_address_street)
c.drawString(65, pageheight - 195, customer_address_city)
c.drawString(65, pageheight - 205, customer_address_state)


# table
#data.insert(0,['S.NO', 'Name of plant', 'size of plant', 'quantity', 'price per item', 'Amount'])
tbl=Table(data, colWidths=[45,120,80,100,100])
tbl.setStyle(TableStyle([
                       ('BACKGROUND',(0,0),(-1,0),HexColor("#C0C0C0")),
                       ('GRID',(0,1),(-1,-1),0.01*inch,(0,0,0,)),
                       ('FONT', (0,0), (-1,0), 'Helvetica-Bold')]))

for i in data:
    if i!=0:
        print(data)
table_top_height=260
table_height=len(data)
print('table_height',table_height)

#print table
tbl.wrapOn(c,500,500)
tbl.drawOn(c, 25,pageheight-(table_height*15)-table_top_height)

# total
c.setFont('Cooper',12)
c.drawString(390,pageheight-(table_height*15)-table_top_height-20,'total amount: Rs '+str(total_bill))
c.setFont('Calibri', 12)
# thankyou
c.drawString(250,pageheight-(table_height*15)-table_top_height-50, "Thank you, visit again!")

# creating the file
c.save()

#open pdf file
os.system(r'C:\Users\vvsnm\PycharmProjects\DesktopOne\firstfile.pdf')
print('file opened')

