# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 13:55:37 2018

@author: Tanmay
"""
import datetime
import smtplib
#from tabulate import tabulate
from jinja2 import Environment
import email.message
from html import HTML
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import xlrd
def get_subjects(data,x,y):
    count=0
    j=y+1
    while data[x][j]!="PROCTOR" and data[x][j]!="Total" and data[x][j]!="per" :
        if data[x][j]!="":
           print data[x][j]
           count=count+1
           #print(data[x][j])
        j=j+1;
        
        if j==len(data[x]):
            break
    return count

def make_lec(data,x,y,subjects,suby,pery,month):
    header=list()
    header.append(data[x][y])
    j=month
    p=pery
    count=subjects
    
    while count!=0:
        monthCount=month
        while(monthCount>=0):
            if(data[x][j]!=""):
                header.append(data[x][j])
                j=j+1
            monthCount=monthCount-1
        print(p-1)
        print(data[x][p-1])
        header.append(data[x][p-1])
        
       
        header.append(data[x][p])
        count=count-1
        j=j+5-month
        p=p+6
    p=p-5
    header.append(data[x][p])
    header.append(data[x][p+1])
    header.append(data[x][p+2])
    print header
    return header
def make_month(data,x,y,subjects,month):
    header=list()
   
    header.append("Month")
    while subjects!=0:
        j=y
        monthCount=month
        while(monthCount>=0):
            header.append(data[x][j])
            j=j+1
            monthCount=monthCount-1
        header.append("total")
        header.append("%")
        subjects=subjects-1
    header.append("")
    header.append("")
    header.append("")
    #print(header)
    return header
    
    
    
def make_row(data,x,y):
    header=list()
    for i in range(len(data[x])):
        if data[x][i]!="":
            header.append(data[x][i])
    #print(header)
    return header
    
    
    
def get_excel_data(sheet_name,year,sem):
    book_name = "Attendance_"+year+"_"+sem+".xlsx"
    #book_name="test.xlsx"
    workbook = xlrd.open_workbook(book_name)
    #sheet_name="SY BTech-A"
    worksheet= workbook.sheet_by_name(sheet_name)
    table=list()
    record = list()
    for x in range(worksheet.nrows):
        for y in range(worksheet.ncols):
            record.append(worksheet.cell(x,y).value)
        table.append(record)
        record =[]
        x+=1
        
    return table

def get_email_roll(sheetname,roll):
    workbook = xlrd.open_workbook('email.xlsx')
    worksheet= workbook.sheet_by_name(sheetname)
    
    rolly=0
    emaily=0
    emailReturn="dummy"
    for x in range(worksheet.nrows):
        for y in range(worksheet.ncols):
            if worksheet.cell(x,y).value=="Roll No":
                rolly=y
            if worksheet.cell(x,y).value=="email":
                emaily=y
    for x in range(worksheet.nrows):
        for y in range(worksheet.ncols):
             if worksheet.cell(x,y).value==roll:
                 emailReturn=worksheet.cell(x,emaily).value
    return emailReturn
    
def send_defaulter_mail(send_emailid,header,data2,subjects,month,sheetname):
        now = datetime.datetime.now()
        h=HTML()
        t = h.table(border='2',cellpadding="10",style='border-collapse:collapse')
        r = t.tr
        r.th(str(header[0][0]),colspan='2')
        i=1
        while(subjects!=0):
            print(month)
            r.th(str(header[0][i]),colspan=str(month+3))
            subjects=subjects-1
            i=i+1
        for x in range(i,len(header[0])):
            r.th(str(header[0][x]))
        r = t.tr
        r.th(str(header[1][0]),colspan='2')
        for x in range(1,len(header[1])):
            r.th(str(header[1][x]))
        r = t.tr
        r.th(str(header[2][0]),colspan='2')
        for x in range(1,len(header[2])):
            r.th(str(header[2][x]),rowspan="2")
        
        r = t.tr
        r.th("Roll Number")
        r.th("Name of the student")
        
        
        r = t.tr
        flagRoll=0
        roll=0
        percentage=0
        for x in range(len(data2)):
            r.td(str(data2[x]))
            percentage=data2[x]
            if flagRoll==0:
                roll=data2[x]
                flagRoll=1
        
        """ 
        for i in range(len(header)):
            r = t.tr
            for j in range(len(header[i])):
                r.th(str(header[i][j]),rowspan='2')"""
                
        #print(t)
        #print(percentage)
        # print(header)
        msg=MIMEMultipart('alternative')
        #msg=email.message.Message()
        msg['From']="tanmay.bid1@gmail.com"
        msg['To']=send_emailid
        msg['Subject']='Python Table Mail'
        body="hi roshni"
        
      
        strat="sub0='DS',sub1='DS'"
        data="dms"
        MyMessage="Dear Sir/Madam,<br> Please find below theory subject attendance details for the month.<br><br> "
        HTML_BODY=MIMEText(MyMessage+str(t),'html');
        msg.attach(HTML_BODY)
        #msg.add_header('Content_Type','text/html')
        #msg.set_payload(content)
        #msg.attach(MIMEText(body,'plain'))
        text=msg.as_string()
        mail=smtplib.SMTP_SSL('smtp.gmail.com',465)
        #mail.ehlo()
        #mail.starttls()
        mail.login('tanmay.bid1@gmail.com','bidbid123')
        if percentage<75:
            get_email_roll(sheetname,roll)
            mail.sendmail('tanmay.bid1@gmail.com',send_emailid,text)
        mail.quit()
        
def emailFunction(sem,month,sheetname,year):
    flagper=0
    flagmonth=0
    
    data=get_excel_data(sheetname,year,sem)
    #print data
    #month=1
    #sem="ODD"
    number_of_subjects=5
    for x in range(len(data)/number_of_subjects):
        for y in range(len(data[x])):
            if data[x][y]=="per":
                total=y
            if data[x][y]=="Roll No":
                rollx=x+1
                rolly=y
            if data[x][y]=="Subjects":
                subx=x;
                suby=y;
            if sem=="ODD":
                if data[x][y]=="Jul":
                    if flagmonth==0:
                        monthy=y
                        monthx=x
                        flagmonth=1
            else:
                if data[x][y]=="Jan":
                    if flagmonth==0:
                        monthy=y
                        monthx=x
                        flagmonth=1
            if data[x][y]=="No of lecture conducted":
                lecx=x
                lecy=y
            if data[x][y]=="%":
                if flagper==0:
                    pery=y
                    perx=x
                    flagper=1
            
                
                
    header=list()
    data2=list()
    subjects=get_subjects(data,subx,suby)
    print subjects
    
    print "$$"
    #print(data[lecx][lecy])
    header.append(make_row(data,subx,suby))
    header.append(make_month(data,monthx,monthy,subjects,month))
    header.append(make_lec(data,lecx,lecy,subjects,suby,pery,month))
    header.append(data[rollx-1][rolly])
    #print(header)
    """
    for p in range(rollx-4,rollx-1):
        for q in range(len(data[p])):
            if(data[p][q]!=""):
                data2.append(data[p][q])
        header.append(data2)
        data2=[]
    """
    #total students strt
    book_name = "test.xlsx"
    workbook = xlrd.open_workbook(book_name)
    sheets = workbook.sheets()

    for sheet in sheets:
        print sheet.name
        if(sheet.name == sheetname):
            students = sheet.nrows-10
            print sheetname
    #total students
    total_students=students
    #total_students=1
    for i in range(rollx,rollx+total_students):
        data2.append(str(int((data[i][rolly]))))
        data2.append(data[i][rolly+1])
        j=monthy
        p=pery
        
        count=subjects
        while count!=0:
            monthCount=month
            
            while(monthCount>=0):
                if(data[i][j]!=""):
                    data2.append(data[i][j])
                    j=j+1
                monthCount=monthCount-1
            data2.append(data[i][p-1])
            data2.append(data[i][p])
            count=count-1
            j=j+5-month
            p=p+6
        for j in range(p-5,len(data[i])):
            if(data[i][j]!=""):
                data2.append(data[i][j])
        send_defaulter_mail("tanmay.bid1@gmail.com",header,data2,subjects,month,sheetname)
        #print("heere")
        #print(data2)
        data2=[]
    
    return "sent"
        
