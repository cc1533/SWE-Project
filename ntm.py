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
#       0.  Fix MalletCaller.py to process mallet correctly... (my bad)
#               - It processes mallet to completion but for some reason disregards the # of topics
#       1.  Display models
#               - Figure out how to send radio button states as arguments to modeler
#               - Send radio button states, # of topics and type of model to modeler?
#               - Figure out how to display the model in the GUI
#                   -- A new image widget?
#       2.  Testing on Windows / Linux
#               - Everything works on Linux up to displaying the models but that has not been implemented yet.
#       3.  Non-Functional Requirements
#               - Clean up code, unify formatting across all modules
#               - GUI changes to make it more intuitive, simplified?
#               - Add some kind of progress bar or loading spinner when other modules are processing
#                   -- There are notifications when the processes are done but not during processing
#                   -- It would just be "nicer" as a user to tell that stuff is happening in the program
#               - Any reason for us to have a menu bar?  How would it be used?  How would it make user's lives easier?
#               - Security issues:
#                   -- [None, at the moment]
#               - Performance Testing:
#                   -- Performance while idle
#                   -- Performance while processing
#                   -- Performance while the final model is displayed
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

        ########################################################################################################
        ''''
        Excel to Parser Function
        This function takes the contents of the Excel file and converts the data into a plaintext document.
        ''''
        ########################################################################################################

        # Create input file label, text line, search button and the parser button
        inputLabel = QLabel('Input Excel File Location:')
        self.inputLine = QLineEdit('/Path/To/Input/File')
        self.inputLine.setReadOnly(True)
        self.inputLine.setToolTip('This is the path to the input file Mallet should process.')
        self.inputSearch = QPushButton("...")
        self.inputSearch.setToolTip('Find the file Mallet should process.')
        self.inputSearch.clicked.connect(self.fileSearch)

        # Create mallet label, text line, search button and call mallet button
        malletLabel = QLabel('Mallet Location:')
        self.malletLine = QLineEdit('/Path/To/Mallet/Program')
        self.malletLine.setReadOnly(True)
        self.malletLine.setToolTip('This is the path to where the Mallet program is located.')
        self.malletSearch = QPushButton("...")
        self.malletSearch.setToolTip('Find the Mallet program.')
        self.malletSearch.clicked.connect(self.fileSearch)
        self.malletSearch.setEnabled(False)

        # Create Run button to parse input file and call mallet
        self.runButton = QPushButton('Execute')
        self.runButton.setToolTip('Parses Excel Input File and Calls Mallet')
        self.runButton.clicked.connect(self.runProg)
        self.runButton.setEnabled(False)

        # Create check boxes, these will be used later
        self.enhCheck = QRadioButton('View Enhancements')
        self.enhCheck.setChecked(True)
        self.enhCheck.setToolTip('Show Enhancements?')
        self.bugCheck = QRadioButton('View Bugs')
        self.bugCheck.setChecked(False)
        self.bugCheck.setToolTip('Show Bugs?')

        # Create spin box widget to get the # of desired topics displayed in the model
        numTopicLabel = QLabel('Number of Topics:  ')
        self.numTopicBox = QSpinBox()
        self.numTopicBox.setRange(1, 20)        # Arbitrarily picked 20, idk what the max should be
        self.numTopicBox.setToolTip('Number of topics to be displayed (10 by default).')
        self.numTopicBox.setValue(10)

        # Looking for some widget to use to change model types
        self.graphTypeBox = QComboBox()
        graphTypeList = ['Line', 'Bar', 'Pie']
        self.graphTypeBox.insertItems(0, graphTypeList)
        self.graphTypeBox.setToolTip('Choose what kind of graph the data should be displayed as.')

        # Create layout boxes (makes things line up nicely)
        vBox1 = QVBoxLayout()
        hBox1 = QHBoxLayout()
        hBox2 = QHBoxLayout()

        # Add the first set of widgets to the window (input file stuff)
        vBox1.addWidget(inputLabel)
        hBox1.addWidget(self.inputLine)
        hBox1.addWidget(self.inputSearch)
        vBox1.addLayout(hBox1)

        # Add # of topics box
        hBox3 = QHBoxLayout()
        hBox3.addWidget(numTopicLabel)
        hBox3.addWidget(self.numTopicBox)
        vBox1.addLayout(hBox3)

        # Add the second set of widgets to the window (mallet stuff)
        vBox1.addWidget(malletLabel)
        hBox2.addWidget(self.malletLine)
        hBox2.addWidget(self.malletSearch)
        vBox1.addLayout(hBox2)
        vBox1.addWidget(self.runButton)

        # Add checkboxes and other widgets to window
        hBox3 = QHBoxLayout()
        hBox3.addWidget(self.enhCheck)
        hBox3.addWidget(self.bugCheck)
        vBox1.addLayout(hBox3)
        # vBox1.addWidget(self.graphTypeBox)

        mainLayout = QGridLayout()
        mainLayout.addLayout(vBox1, 0, 1)

        self.setLayout(mainLayout)
        self.setWindowTitle('Next Top Model')

    def runProg(self):
        print('GUI - Run button pressed.')
        malletPath = str(self.malletLine.text())
        inputFilePath = str(self.inputLine.text())

        print('GUI - Testing Mallet Path...')
        # checks for valid mallet path first
        if malletPath == '':
            QMessageBox.information(self, 'Error',
                                    'No path found.  Please enter the Mallet Program.')
            return
        elif 'mallet' not in malletPath:
            QMessageBox.information(self, 'Error',
                                    'Mallet not found in path.  Please enter the Mallet Program.')
            return
        else:
            print('GUI - Valid mallet path found, testing input file path.')

            # if the mallet path is valid, check input file path
            if inputFilePath == '':
                QMessageBox.information(self, 'Error',
                                        'No path found.  Please enter the input file path.')
                return

            elif '.xls' not in inputFilePath and '.xlsx' not in inputFilePath:
                QMessageBox.information(self, 'Error',
                                        'Valid Excel File not found.  Please enter a valid input file.')
                return

            else:
                # if both paths are valid, go ahead and run the modules
                print('GUI - Input File and Mallet paths are valid, running...')

                # Call Parser
                print('GUI - ExcelParser.py executing -- Please Wait.')
                import ExcelParser
                ExcelParser.main(inputFilePath, '1', '"3 4"')

                # Call MalletCaller.py
                print('GUI - MalletCaller.py executing -- Please Wait.')
                import MalletCaller
                MalletCaller.main(malletPath, str(self.numTopicBox.value()))

                # Call FileFilter.py
                print('GUI - FileFilter.py executing -- Please Wait.')
                import FileFilter
                FileFilter.main()

                # Call TopicStocker.py
                print('GUI - TopicStocker.py executing -- Please Wait.')
                import TopicStocker
                TopicStocker.main(str(self.numTopicBox.value()))

                print('GUI - All modules done processing.')
                QMessageBox.information(self, 'Processing Completed', 'Modules have finished processing.')

    def fileSearch(self):
        print('GUI - File Search button pressed')
        fname = QFileDialog.getOpenFileName(self, 'Open file')

        fname1 = str(fname).split()

        inputLen = len(fname1[0])               # we need to know how long the input is
        inputLen -= 2                                   # get rid of the last two characters ',
        inputFile = fname1[0][2:inputLen]    # strip off the first two characters ('

        # These print statements show exactly what the problem was and how it was progressively resolved
        # print(str(fname))
        # print(fname1[0])
        # print(inputfile)

        print('GUI - Testing:  ' + inputFile)
        # Is the input the mallet path or the input file path?
        if 'Mallet' in inputFile or 'mallet' in inputFile:
            print('GUI - Mallet input path detected, setting Mallet line.')
            self.malletLine.setText(inputFile)
            self.runButton.setEnabled(True)
            return
        elif '.xls' in inputFile or '.xlsx' in inputFile:
            print('GUI - Excel input path detected, setting Excel line.')
            self.inputLine.setText(inputFile)
            self.malletSearch.setEnabled(True)
            return
        else:
            QMessageBox.information(self, 'Error', 'Please enter a valid input file')
            return

# code below looks for inputdirectory in the program path location, if it is not found, the program makes one
ipDir = 'inputdirectory'
if not os.path.exists(ipDir):
    print('GUI - No Input Directory Found, Creating Input Directory')
    os.makedirs(ipDir)      # Chris:  I'm pretty sure this will work just fine on Windows as well
else:
    print('GUI - Input Directory Found.')

if __name__ == '__main__':
    import sys
 
    app = QApplication(sys.argv)
 
    screen = Form()
    screen.show()
 
    sys.exit(app.exec_()) 

