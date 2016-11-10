#####################################################################################################
# 	CSE 4214, Intro to Software Engineering, Fall 2016
# 	Lab Section 2, Group 3, Next Top Model
#
#####################################################################################################
# 	Contributors:
# 			Alex Palacio, Christopher Cole, Jia Zhao,
# 			Nathan Frank, Reid Montague, Titus Dillon
#
#####################################################################################################
#  TODO:
#       1.  Add Call Mallet button functionality
#       2.  Test to make sure it runs and works correctly on Windows
#       3.  Figure out how to get the graphing stuff to work?
#
#####################################################################################################
#  Program info:
# 	- This is the GUI that the user will interface with and drive the program.
#
#####################################################################################################
# !/usr/bin/python

from subprocess import call
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
 
class Form(QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        # setGeometry(self, ax, ay, aw, ah) -> x, y, width, height
        x = 300
        y = 200
        self.setGeometry(x, y, x, y)

        # Create input file label, text line, search button and the parser button
        inputlabel = QLabel("Input File Location:")
        self.inputline = QLineEdit("/Path/To/Input/File.xlsx")
        self.inputline.setReadOnly(True)
        self.inputline.setToolTip("This is the path to the input file Mallet should process.")
        self.inputSearch = QPushButton("...")
        self.inputSearch.setToolTip("Find the file Mallet should process.")
        self.inputSearch.clicked.connect(self.fileSearch)
        self.parse = QPushButton("Parse Input")
        self.parse.setToolTip("Every input file must be parsed before it can be processed by Mallet")
        self.parse.clicked.connect(self.callParseButton)

        # Create mallet label, text line, search button and call mallet button
        malletlabel = QLabel("Mallet Location:")
        self.malletline = QLineEdit("/Path/To/Mallet")
        self.malletline.setReadOnly(True)
        self.malletline.setToolTip("This is the path to where the Mallet program is located.")
        self.malletSearch = QPushButton("...")
        self.malletSearch.setToolTip("Find the Mallet program.")
        self.malletSearch.clicked.connect(self.fileSearch)
        self.callmallet = QPushButton("Call Mallet")
        self.callmallet.setToolTip("Mallet must be called so it can process the the input file.")
        self.callmallet.clicked.connect(self.callMalletButton)

        # Create check boxes, these will be used later
        self.enhCheck = QCheckBox("View Enhancements")
        self.enhCheck.setToolTip("Show Enhancements?")
        self.bugCheck = QCheckBox("View Bugs")
        self.bugCheck.setToolTip("Show Bugs?")

        # Create layout boxes (makes things line up nicely)
        vLayout = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()

        # Add the first set of widgets to the window (input file stuff)
        vLayout.addWidget(inputlabel)
        hbox1.addWidget(self.inputline)
        hbox1.addWidget(self.inputSearch)
        vLayout.addLayout(hbox1)
        vLayout.addWidget(self.parse)

        # Add the second set of widgets to the window (mallet stuff)
        vLayout.addWidget(malletlabel)
        hbox2.addWidget(self.malletline)
        hbox2.addWidget(self.malletSearch)
        vLayout.addLayout(hbox2)
        vLayout.addWidget(self.callmallet)

        # Add checkboxes and other widgets to window
        vLayout.addWidget(self.enhCheck)
        vLayout.addWidget(self.bugCheck)
 
        mainLayout = QGridLayout()
        # mainLayout.addWidget(nameLabel, 0, 0)
        mainLayout.addLayout(vLayout, 0, 1)
        #mainLayout.addLayout(hLayout, 0, 1)
 
        self.setLayout(mainLayout)
        self.setWindowTitle("Next Top Model")
 
    def callMalletButton(self):
        name = self.malletline.text()
 
        if name == "":
            QMessageBox.information(self, "Error",
                                    "Please enter the Mallet Program.")
            return
        elif "mallet" not in name:
            QMessageBox.information(self, "Error", "Please enter the Mallet Program.")
        else:
            QMessageBox.information(self, "Mallet Called", "Please wait as Mallet processes your input file.")
            return
    
    def callParseButton(self):
        inputFile = self.inputline.text()
 
        if inputFile == "":
            QMessageBox.information(self, "Error",
                                    "Please enter the Input file.")
            return
        elif ".xls" not in inputFile or ".xlsx" not in inputFile:
            QMessageBox.information(self, "Error", "Please enter a valid input file.")
        else:
            QMessageBox.information(self, "Valid Input File",
                                    "Parsing %s for Mallet" % inputFile)
            # I think this call needs to be simplified:  reduce "malletInputFile.txt" and chance "EXCEL.txt"
            # call(["python3.5", "ExcelParser.py", inputFile, "malletInputFile.txt", "1", "EXCEL.txt", "3 4"])
            return

    def fileSearch(self):
        # QFileDialog.getOpenFileName probably gets us as close to a decent path + filename as we can get
        # But it requires some clever formatting to get it to a usable string
        fname = QFileDialog.getOpenFileName(self, 'Open file')

        fname1 = str(fname).split()
        # str(fname) returns ('/path/to/file', All Files (*)')
        # so str(fname).split() is used to get ('/path/to/file' by itself so it can  be parsed easier

        inputlen = len(fname1[0])               # we need to know how long the input is
        inputlen -= 2                                   # get rid of the last two characters ',
        inputfile = fname1[0][2:inputlen]    # strip off the first two characters ('

        # These print statements show exactly what the problem was and how it was progressively resolved
        print(str(fname))
        print(fname1[0])
        print(inputfile)

        if "mallet" in inputfile:
            self.malletline.setText(inputfile)
            return
        elif ".xls" in inputfile or ".xlsx" in inputfile:
            self.inputline.setText(inputfile)
            return
        else:
            QMessageBox.information(self, "Error", "Please enter a valid input file")
            return
        # self.inputline.setText(fname)

    # This will be the function that displays the generated graphs
    # def showGraph(self):
        # return


if __name__ == '__main__':
    import sys
 
    app = QApplication(sys.argv)
 
    screen = Form()
    screen.show()
 
    sys.exit(app.exec_()) 
