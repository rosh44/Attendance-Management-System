# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 19:58:17 2018

@author: Rushabh
"""

import sheetScan.demo as hi
import cv2
import xlrd
import xlsxwriter as ex
from os.path import expanduser
home = expanduser("~")

def countAtt():
    img = cv2.imread('scan11.jpeg')
    print "Front: "
    farr = hi.front(img)
    print(farr)
    
    img = cv2.imread('scan21.jpeg')
    print "Back: "
    barr = hi.back(img)
    print(barr)
    
    totarr = farr+barr
    return totarr

def totalAtt():
    path = "C:/Users/Rushabh/.spyder-py3/Attendance/Scripts"
    front_imgs = ['/scan11.jpeg','/scan12.jpeg']
    for i in front_imgs:
        img_path = path+i
        img = cv2.imread(img_path)
        print "Front: "
        if front_imgs.index(i) == 0:
            farr = hi.front(img)
        else:
            farr = farr + hi.front(img)
        print(farr)

def make_Header(workbook,worksheet,table):
    cell_format = workbook.add_format({'align': 'center',
                                   'valign': 'center',
                                   'font_name':'Arial',
                                   'font_size':16,
                                   'bold': True,
                                   'border': 2})
    for i in range(5):
        for j in range(len(table[i])):
            worksheet.merge_range(i,0,i,20, table[i][j], cell_format) 
    bold = workbook.add_format({'bold': True,'align': 'center','border': 1})
    worksheet.merge_range(6,0,6,2, table[6][0], bold)
    subjects=5
    j=1
    k=3
    
    while(subjects!=0):
         worksheet.merge_range(6,k,6,k+5, table[6][j], bold)
         k=k+6
         j=j+1
         subjects=subjects-1
    worksheet.write(6,k,'PROCTOR',bold)
    worksheet.write(6,k+1,'Total',bold)
    worksheet.write(6,k+2,'Total %',bold)
    worksheet.merge_range(7,0,7,2, table[7][0], bold)
    for x in range(1,len(table[7])):
        worksheet.write(7,x+2,table[7][x],bold)
    worksheet.write(7,x+3,"",bold)
    worksheet.write(7,x+4,"",bold)
    worksheet.write(7,x+5,"",bold)  
    month=1
    worksheet.merge_range(8,0,8,2, table[8][0], bold)
    
    for i in range(1,len(table[8])):
        worksheet.merge_range(8,i+2,9,i+2, table[8][i], bold)
    worksheet.write(9,0,"Sr no.",bold)
    worksheet.write(9,1,"Roll No",bold)
    worksheet.write(9,2,"Student Name",bold)    
    
def get_excel_data(workbook, worksheet):
    table=list()
    record = list()
    for x in range(worksheet.nrows):
        for y in range(worksheet.ncols):
            if(worksheet.cell(x,y).value!=""):
                record.append(worksheet.cell(x,y).value)
            else :
                if(x==8 and y>=4):
                    record.append(worksheet.cell(x,y).value)
        table.append(record)
        record =[]
        x+=1
        
    return table

def fillColumn(sheetname,subj,month):
    totarr = countAtt()
    
    workbook = xlrd.open_workbook('attendanceFinal.xlsx'.format(home))
    sheets = workbook.sheets()
    
    writebook = ex.Workbook('test.xlsx')
    
    #data.to_excel('odd18(2).xlsx')
#    
#    sheetname = 'SY BTech-A'
#    subj = 0
#    month = 2
    ucol = int(3+(subj*6)+int(month))
    
    print(totarr)
    print('lec'+str(totarr[4]))
    
    flag=0
    
    for sheet in sheets:
        newSheet = writebook.add_worksheet(sheet.name)
        table = get_excel_data(workbook,sheet)
        if(flag==0):
            flag = 1
            print table[8]
            
        print len(table[8])
        make_Header(writebook, newSheet, table)
        for row in range(10,sheet.nrows):
            for col in range(sheet.ncols-1):
                if(col<3): 
                    newSheet.write(row, col, sheet.cell(row,col).value)
                else:
                    newSheet.write(row, col, sheet.cell(row,col+1).value)
        if(sheet.name == sheetname):
            bold = writebook.add_format({'bold': True,'align': 'center','border': 1})
            newSheet.write(8,ucol,int(totarr[0]),bold)
            for x in range(10,sheet.nrows):
                newSheet.write(x,ucol,int(totarr[(x-9)%(len(totarr)-1)]))
       
    writebook.close()
