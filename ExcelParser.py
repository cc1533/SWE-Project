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
#                       - parse the .xlsx to a plain text (.txt) file
#                       - parse a specified column to a plain text (.txt) file
#
#####################################################################################################
#!/usr/bin/python
'''


#-------------------------------------------------
#
# retrieval from passed in GUI inputs
#
#-------------------------------------------------
#
# input values retrieved from the user via the GUI may be passed in via this function
#
# stockInputs(ExcelDocument, ParsedColumnOutputFilename, ColumnToBeParsed, ExcelTextOutputFilename, ExcelDateColumns)
#
#-------------------------------------------------

def stockInputs():
    return


#-------------------------------------------------
#
# retrieval from command line arguments
#
#-------------------------------------------------
#
# Index Key:
#       0 - Python File Name
#       1 - Excel Input File
#       2 - Parsed Column Output File Name (including file extension) 
#       3 - Column to be Parsed
#       4 - Text Excel File Name [OPTIONAL] (will have a default)
#       5 - Excel Date Columns [OPTIONAL]
#
# Command Format: python ExcelParser.py [ExcelDocument] [ParsedColumnOutput] [ColumnNumber] [ExcelTextOuput] ["DateColumns"]
#       - without brackets
#
# Sample Command: python ExcelParser.py Firefox_MasterFile_4214Fall2016.xlsx TOPICINPUT.txt 1 EXCEL.txt "3 4"
#
#-------------------------------------------------
from sys import argv

def getCommandInputs():
    
    argList = argv

    excelInputPath = argList[1]

    colOutputPath = argList[2]
    colToParse = argList[3]

    ETOutputPath = argList[4]
    dateCols = argList[5].split()

    return excelInputPath, colOutputPath, colToParse, ETOutputPath, dateCols
#-------------------------------------------------


import xlrd
import datetime


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
        
    def parseColumn(self, column, outputfile):

        if (self.__book == ""):
            return 0

        sheet = self.__book.sheet_by_index(0)
        self.__comments = []

        rowCount = sheet.nrows

        for row in range(1, rowCount): #skips the heading
            
            content = str(sheet.cell(row, column).value)
            content += " "
            self.__comments.append(content)

        
        outputfile2 = outputfile.replace(".txt", ".lined")
        
        # writes the contents of the column to file for mallet topic training
        file = open(outputfile, "w")
        file2 = open(outputfile2, "w")
        
        for line in self.__comments:
            file.write(str(line))
            file2.write(str(line) + '\n')
               
        file.close()
        file2.close()

        return 1
        
    def createExcelText(self, outputPath, dateCols = []):

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

        #outputFile.write('\n') #creates table

        for row in range(1, rowCount):
            
            for column in range(colCount):

                content = sheet.cell(row, column).value

                isDateCol = column in self.__dateColumns
                isNotEmpty = (content != "" and content != "null" and content != None)

                if (isDateCol and isNotEmpty):
                    
                    year, month, day, hour, minute, second = xlrd.xldate_as_tuple(content, self.__book.datemode)
                    content = datetime.date(year, month, day)
                    
                outputFile.write(str(content) + delimiter)

            #outputFile.write("\n") #creates table

        outputFile.close()

        return 1


excelInputPath = 'Firefox_MasterFile_4214Fall2016.xlsx'
colOutputPath = 'inputdirectory\\TOPICINPUT.txt'
colToParse = 1
ETOutputPath = 'EXCEL.txt'
dateCols = [3,4]

#excelInputPath, colOutputPath, colToParse, ETOutputPath, dateCols = getCommandInputs()


test = ExcelParser()
test.submitFile(excelInputPath)

# creates .txt file from descriptions
test.parseColumn(colToParse, colOutputPath)

# creates .txt file from entire input file
test.createExcelText(ETOutputPath, dateCols)

