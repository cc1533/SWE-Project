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
#       1.  Add full button functionality
#           - Call Mallet button needs to call mallet
#           - Check boxes functionality
#           - *add a new* display model button, basically call the VisualModeler?
#           - # of topics to display widget (spin box?), sends arguments to MalletCaller and TopicStocker
#       2.  Test to make sure it runs and works correctly on Windows
#           - Make sure that everything that uses paths can work on Windows and Linux
#       3.  Figure out how to get the model stuff to be displayed?
#           - Just open them in any image viewer?
#           - Create image widget in the GUI and display it there?
#           - Interactive ggplot window displayed?
#       4.  Make sure all calls to external modules work
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
import os


class Form(QWidget):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        # setGeometry(self, ax, ay, aw, ah) -> x, y, width, height
        x = 300
        y = 200
        self.setGeometry(x, y, x, y)

        # Create input file label, text line, search button and the parser button
        inputLabel = QLabel("Input File Location:")
        self.inputLine = QLineEdit("/Path/To/Input/File")
        self.inputLine.setReadOnly(True)
        self.inputLine.setToolTip("This is the path to the input file Mallet should process.")
        self.inputSearch = QPushButton("...")
        self.inputSearch.setToolTip("Find the file Mallet should process.")
        self.inputSearch.clicked.connect(self.fileSearch)
        self.parseButton = QPushButton("Parse Input")
        self.parseButton.setToolTip("Every input file must be parsed before it can be processed by Mallet")
        self.parseButton.clicked.connect(self.callParseButton)
        self.parseButton.setDisabled(True)

        # Create mallet label, text line, search button and call mallet button
        malletLabel = QLabel("Mallet Location:")
        self.malletLine = QLineEdit("/Path/To/Mallet/Program")
        self.malletLine.setReadOnly(True)
        self.malletLine.setToolTip("This is the path to where the Mallet program is located.")
        self.malletSearch = QPushButton("...")
        self.malletSearch.setToolTip("Find the Mallet program.")
        self.malletSearch.clicked.connect(self.fileSearch)
        self.malletButton = QPushButton("Call Mallet")
        self.malletButton.setToolTip("Mallet must be called so it can process the the input file.")
        self.malletButton.clicked.connect(self.callMalletButton)
        self.malletButton.setDisabled(True)

        # Create check boxes, these will be used later
        self.enhCheck = QCheckBox("View Enhancements")
        self.enhCheck.setChecked(True)
        self.enhCheck.setToolTip("Show Enhancements?")
        self.bugCheck = QCheckBox("View Bugs")
        self.bugCheck.setChecked(True)
        self.bugCheck.setToolTip("Show Bugs?")

        # Create spin box widget to get the # of desired topics displayed in the model
        self.numTopicBox = QSpinBox()
        self.numTopicBox.setRange(1, 20)        # Arbitrarily picked 20, idk what the max should be
        self.numTopicBox.setToolTip("Number of topics to be displayed (10 by default).")
        self.numTopicBox.setValue(10)

        # Looking for some widget to use to change model types
        self.graphTypeBox = QComboBox()
        graphTypeList = ['Line', 'Bar', 'Pie']
        self.graphTypeBox.insertItems(0, graphTypeList)
        self.graphTypeBox.setToolTip("Choose what kind of graph the data should be displayed as.")


        # Create layout boxes (makes things line up nicely)
        vBox1 = QVBoxLayout()
        hBox1 = QHBoxLayout()
        hBox2 = QHBoxLayout()

        # Add the first set of widgets to the window (input file stuff)
        vBox1.addWidget(inputLabel)
        hBox1.addWidget(self.inputLine)
        hBox1.addWidget(self.inputSearch)
        vBox1.addLayout(hBox1)
        vBox1.addWidget(self.parseButton)

        # Add the second set of widgets to the window (mallet stuff)
        vBox1.addWidget(malletLabel)
        hBox2.addWidget(self.malletLine)
        hBox2.addWidget(self.malletSearch)
        vBox1.addLayout(hBox2)
        vBox1.addWidget(self.malletButton)

        # Add checkboxes and other widgets to window
        hBox3 = QHBoxLayout()
        hBox3.addWidget(self.enhCheck)
        hBox3.addWidget(self.bugCheck)
        vBox1.addLayout(hBox3)
        vBox1.addWidget(self.numTopicBox)
        vBox1.addWidget(self.graphTypeBox)

        mainLayout = QGridLayout()
        # mainLayout.addWidget(nameLabel, 0, 0)
        mainLayout.addLayout(vBox1, 0, 1)
        #mainLayout.addLayout(hLayout, 0, 1)
 
        self.setLayout(mainLayout)
        self.setWindowTitle("Next Top Model")
 
    def callMalletButton(self):
        name = self.malletLine.text()
 
        if name == "":
            QMessageBox.information(self, "Error",
                                    "Please enter the Mallet Program.")
            return
        elif "Mallet" not in name:
            QMessageBox.information(self, "Error", "Please enter the Mallet Program.")
        else:
            QMessageBox.information(self, "Mallet Called", "Please wait as Mallet processes your input file.")

            if (os.name == "nt"):
                # calls for Windows machines
                call(["python", "MalletCaller.py", str(self.numTopicBox.value())], shell=True)
                call(["python", "FileFilter.py"], shell=True)
                call(["python", "TopicStocker.py", str(self.numTopicBox.value())], shell=True)
            elif (os.name == "posix"):
                # calls for Linux
                call(["python3.5", "MalletCaller.py", str(self.numTopicBox.value())], shell=True)
                call(["python3.5", "FileFilter.py"], shell=True)
                call(["python3.5", "TopicStocker.py", str(self.numTopicBox.value())], shell=True)
            else:
                print('Warning, Operating System is not supported.')

            # I thought this was appropriate because it takes a little while for everything to finish
            QMessageBox.information(self, "Processing Completed", "Mallet has finished processing.")
            return
    
    def callParseButton(self):
        inputFile = self.inputLine.text()
 
        if inputFile == "":
            QMessageBox.information(self, "Error",
                                    "Please enter the Input file.")
            return
        elif ".xls" not in inputFile or ".xlsx" not in inputFile:
            QMessageBox.information(self, "Error", "Please enter a valid input file.")
        else:
            QMessageBox.information(self, "Valid Input File",
                                    "Parsing %s for Mallet" % inputFile)

            if (os.name == "nt"):
                # Working call for Windows machines
                # the one and the datelist arguments needed to be separated
                # hopefully this causes an error for Linux
                call(['python', 'ExcelParser.py', inputFile, '1', '"3 4"'], shell=True)
            elif (os.name == "posix"):
                # call for Linux machines
                call(['python3.5 ExcelParser.py ' + inputFile + ' 1 "3 4"'], shell=True)
            else:
                print('Warning, Operating System is not supported.')

            # decided to steal this from Titus since it's a good idea
            QMessageBox.information(self, "Processing Completed", "Parser has completed.")            
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
        #print(str(fname))
        #print(fname1[0])
        #print(inputfile)

        if "Mallet" in inputfile:
            self.malletLine.setText(inputfile)
            self.malletButton.setEnabled(True)
            return
        elif ".xls" in inputfile or ".xlsx" in inputfile:
            self.inputLine.setText(inputfile)
            self.parseButton.setEnabled(True)
            #parseReady = True
            return
        else:
            QMessageBox.information(self, "Error", "Please enter a valid input file")
            return
        # self.inputLine.setText(fname)

    # This will be the function that displays the generated graphs
    # def showGraph(self):
        # return


if __name__ == '__main__':
    import sys
 
    app = QApplication(sys.argv)
 
    screen = Form()
    screen.show()
 
    sys.exit(app.exec_()) 

