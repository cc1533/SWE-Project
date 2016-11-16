'''
#####################################################################################################
#	CSE 4214, Intro to Software Engineering, Fall 2016
#	Lab Section 2, Group 3, Next Top Model
#
#####################################################################################################
#	Contributors:
#			Alex Palacio, Christopher Cole, Jia Zhao,
#			Nathan Frank, Reid Montague, Titus Dillon
#
#####################################################################################################
#	Program info:
#			This program will:
#                          - parse the .xlsx to a plain text (.txt) file
#                          - parse a specified column to a plain text (.txt) file
#
#####################################################################################################
#!/usr/bin/python
'''


import xlrd
import datetime
from sys import argv

#-------------------------------------------------
#
# retrieval from command line arguments
#
#-------------------------------------------------
#
# Index Key:
#       0 - Python File Name
#       1 - Excel Input File
#       2 - Column to be Parsed
#       3 - Excel Date Columns
#
# Command Format: python ExcelParser.py [ExcelDocument] [ColumnNumber] ["DateColumns"]
#       - without brackets
#
# Sample Command: python ExcelParser.py Firefox_MasterFile_4214Fall2016.xlsx 1 "3 4"
#
#-------------------------------------------------
def getCommandInputs():

    argList = argv

    excelInputPath = argList[1]
    colToParse = int(argList[2])
    dateCols = argList[3].split()

    return excelInputPath, colToParse, dateCols
#-------------------------------------------------


class ExcelParser():

    def __init__(self):

        self.__comments = []
        self.__inputPath = ""
        self.__book = ""
        self.__dateColumns = []

    def submitFile(self, inputPath):
        
        self.__inputPath = inputPath

        try:
            self.__book = xlrd.open_workbook(self.__inputPath)

        except FileNotFoundError:
            return 0

        else:
            return 1
        
    def parseColumn(self, column = 1, outputfile = "TOPICINPUT.txt"):

        if (self.__book == ""):
            return 0

        sheet = self.__book.sheet_by_index(0)
        self.__comments = []

        rowCount = sheet.nrows

        for row in range(1, rowCount): #skips the heading
            
            content = str(sheet.cell(row, column).value)
            content += " "
            self.__comments.append(content)

        
        linedOutputfile = outputfile.replace(".txt", ".lined")
        
        # writes the contents of the column to file for mallet topic training
        # also writes column contents to separate file in lined format
        malletinput = open("inputdirectory/"+outputfile, "w")
        linedcolumn = open(linedOutputfile, "w")
        
        for line in self.__comments:
            malletinput.write(str(line))
            linedcolumn.write(str(line) + '\n')
               
        malletinput.close()
        linedcolumn.close()

        return 1
        
    def createExcelText(self, dateCols = ["3", "4"], outputPath = "EXCEL.txt"):

        if (self.__book == ""):
            return 0

        sheet = self.__book.sheet_by_index(0)
        outputFile = open(outputPath, "w")
        self.__dateColumns = dateCols

        rowCount = sheet.nrows
        colCount = 5 #sheet.ncols
        
        delimiter = '\t'


        for headerCol in range(colCount):
            outputFile.write(sheet.cell(0, headerCol).value + delimiter)

        outputFile.write('\n') #creates table

        for row in range(1, rowCount):
            
            for column in range(colCount):

                content = sheet.cell(row, column).value

                isDateCol = str(column) in self.__dateColumns
                isNotEmpty = (content != "" and content != "null" and content != None)

                if (isDateCol and isNotEmpty):
                    
                    year, month, day, hour, minute, second = xlrd.xldate_as_tuple(content, self.__book.datemode)
                    content = datetime.date(year, month, day)
                    
                outputFile.write(str(content) + delimiter)

            outputFile.write("\n") #creates table

        outputFile.close()
        return 1


def main(excelInputPath, colToParse, dateCols):

    test = ExcelParser()
    test.submitFile(excelInputPath)

    # creates .txt file from descriptions
    test.parseColumn(colToParse)

    # creates .txt file from entire input file
    test.createExcelText(dateCols)
