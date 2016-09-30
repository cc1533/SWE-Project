import xlrd
import datetime


book = xlrd.open_workbook('Firefox_MasterFile_4214Fall2016.xlsx')
sheet = book.sheet_by_index(0)

for x in range(10):
    print("")
    for y in range(10):
        print(sheet.cell(x,y).value)
