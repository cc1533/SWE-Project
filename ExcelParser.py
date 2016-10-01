import xlrd
import datetime


def excelParse(inputPath, outputPath):

    try:
        book = xlrd.open_workbook(inputPath)

    except FileNotFoundError:
        return 0
    
    sheet = book.sheet_by_index(0)
    outputFile = open(outputPath, "w")

    rowCount = sheet.nrows
    colCount = 5 #sheet.ncols
    # 5 columns is specific to the supplied spreadsheet. row 17528 has 653 columns of what looks like "junk" data

    delimiter = '\t'


    for headerCol in range(colCount):
        outputFile.write(sheet.cell(0, headerCol).value + delimiter)

    outputFile.write('\n')

    for row in range(1, rowCount):
        
        for column in range(colCount):

            content = sheet.cell(row, column).value

            # columns 3 & 4 are date columns specific to supplied spreadsheet
            isDateCol = (column == 3 or column == 4)
            isNotEmpty = (content != "" and content != "null" and content != None)

            if (isDateCol and isNotEmpty):
                
                year, month, day, hour, minute, second = xlrd.xldate_as_tuple(content, book.datemode)
                content = datetime.date(year, month, day)
                
            outputFile.write(str(content) + delimiter)

        outputFile.write("\n")

    outputFile.close()


class ExcelParser():

    def __init__(self):

        self.__comments = []
        self.__filePath = ""
        self.__book = ""

    def submitFile(self, inputPath):
        
        self.__filePath = inputPath

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
        self.__comments = []

        rowCount = sheet.nrows

        for row in range(rowCount):
            content = sheet.cell(row, column).value
            self.__comments.append(content)

        return self.__comments
        
    def createMalletFile(self, outputPath):

        if (self.__book == ""):
            return 0

        sheet = self.__book.sheet_by_index(0)
        outputFile = open(outputPath, "w")

        rowCount = sheet.nrows
        colCount = 5 #sheet.ncols
        
        delimiter = '\t'


        for headerCol in range(colCount):
            outputFile.write(sheet.cell(0, headerCol).value + delimiter)

        outputFile.write('\n')

        for row in range(1, rowCount):
            
            for column in range(colCount):

                content = sheet.cell(row, column).value

                # columns 3 & 4 are date columns specific to supplied spreadsheet
                isDateCol = (column == 3 or column == 4)
                isNotEmpty = (content != "" and content != "null" and content != None)

                if (isDateCol and isNotEmpty):
                    
                    year, month, day, hour, minute, second = xlrd.xldate_as_tuple(content, self.__book.datemode)
                    content = datetime.date(year, month, day)
                    
                outputFile.write(str(content) + delimiter)

            outputFile.write("\n")

        outputFile.close()

        return 1


excelParse('Firefox_MasterFile_4214Fall2016.xlsx', 'malletInputFunctionFile.txt')

test = ExcelParser()
test.submitFile('Firefox_MasterFile_4214Fall2016.xlsx')
test.createMalletFile('malletInputClassFile.txt')
