import xlrd
import datetime


def excelParse():
    
    inputpath = input("Path: ")

    book = xlrd.open_workbook(inputpath)
    sheet = book.sheet_by_index(0)
    outputfile = open("malletInput.txt","w")

    rowCount = sheet.nrows
    colCount = 5 #sheet.ncols
    # 5 columns is specific to the supplied spreadsheet. row 17528 has 653 columns of what looks like "junk" data

    delimiter = '\t'


    for headerCol in range(colCount):
        outputfile.write(sheet.cell(0, headerCol).value + delimiter)

    outputfile.write('\n')

    for row in range(1,rowCount):
        
        for column in range(colCount):

            content = sheet.cell(row, column).value

            # columns 3 & 4 are date columns specific to supplied spreadsheet
            isDateCol = (column == 3 or column == 4)
            isNotEmpty = (content != "" and content != "null" and content != None)

            if (isDateCol and isNotEmpty):
                
                year, month, day, hour, minute, second = xlrd.xldate_as_tuple(content, book.datemode)
                content = datetime.date(year, month, day)
                
            outputfile.write(str(content) + delimiter)

        outputfile.write("\n")

    outputfile.close()


class ExcelParser():

    def __init__(self):

        self.__comments = []
        self.__filePath = ""
        self.__book = ""

    def submitFile(self, filePath):
        
        self.__filePath = filePath

        try:
            self.__book = xlrd.open_workbook(self.__filePath)

        except FileNotFoundError:
            return 0

        else:
            return 1
        
    def parseColumn(self, column):

        if (self.__book == ""):
            return 0

        sheet = self.__book.sheet_by_index(0)
        columnContents = []

        rowCount = sheet.nrows

        for row in range(rowCount):
            content = sheet.cell(row, column).value
            columnContents.append(content)

        return columnContents
        
    def createMalletFile(self):

        if (self.__book == ""):
            return 0

        sheet = self.__book.sheet_by_index(0)
        outputfile = open("malletInput.txt","w")

        rowCount = sheet.nrows
        colCount = 5 #sheet.ncols
        
        delimiter = '\t'


        for headerCol in range(colCount):
            outputfile.write(sheet.cell(0, headerCol).value + delimiter)

        outputfile.write('\n')

        for row in range(1,rowCount):
            
            for column in range(colCount):

                content = sheet.cell(row, column).value

                # columns 3 & 4 are date columns specific to supplied spreadsheet
                isDateCol = (column == 3 or column == 4)
                isNotEmpty = (content != "" and content != "null" and content != None)

                if (isDateCol and isNotEmpty):
                    
                    year, month, day, hour, minute, second = xlrd.xldate_as_tuple(content, self.__book.datemode)
                    content = datetime.date(year, month, day)
                    
                outputfile.write(str(content) + delimiter)

            outputfile.write("\n")

        outputfile.close()

        return 1
