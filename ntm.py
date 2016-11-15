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
#               - Figure out how to send checkboxes' states as arguments to modeler
#               - Send checkbox states, # of topics and type of model to modeler?
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
#                   -- Performance while parsing the excel input file
#                   -- Performance while Mallet is processing
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
# from PyQt5.QtGui import QMovie
import os


class Form(QWidget):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        # setGeometry(self, ax, ay, aw, ah) -> x, y, width, height
        x = 300
        y = 200
        self.setGeometry(x, y, x, y)

        # Create input file label, text line, search button and the parser button
        inputLabel = QLabel('Input File Location:')
        self.inputLine = QLineEdit('/Path/To/Input/File')
        self.inputLine.setReadOnly(True)
        self.inputLine.setToolTip('This is the path to the input file Mallet should process.')
        self.inputSearch = QPushButton("...")
        self.inputSearch.setToolTip('Find the file Mallet should process.')
        self.inputSearch.clicked.connect(self.fileSearch)
        self.parseButton = QPushButton('Parse Input')
        self.parseButton.setToolTip('Every input file must be parsed before it can be processed by Mallet')
        self.parseButton.clicked.connect(self.callParseButton)
        self.parseButton.setDisabled(True)

        # Create mallet label, text line, search button and call mallet button
        malletLabel = QLabel('Mallet Location:')
        self.malletLine = QLineEdit('/Path/To/Mallet/Program')
        self.malletLine.setReadOnly(True)
        self.malletLine.setToolTip('This is the path to where the Mallet program is located.')
        self.malletSearch = QPushButton("...")
        self.malletSearch.setToolTip('Find the Mallet program.')
        self.malletSearch.clicked.connect(self.fileSearch)
        self.malletButton = QPushButton('Call Mallet')
        self.malletButton.setToolTip('Mallet must be called so it can process the the input file.')
        self.malletButton.clicked.connect(self.callMalletButton)
        self.malletButton.setDisabled(True)

        # Create check boxes, these will be used later
        self.enhCheck = QCheckBox('View Enhancements')
        self.enhCheck.setChecked(True)
        self.enhCheck.setToolTip('Show Enhancements?')
        self.bugCheck = QCheckBox('View Bugs')
        self.bugCheck.setChecked(True)
        self.bugCheck.setToolTip('Show Bugs?')

        # Create spin box widget to get the # of desired topics displayed in the model
        self.numTopicBox = QSpinBox()
        self.numTopicBox.setRange(1, 20)        # Arbitrarily picked 20, idk what the max should be
        self.numTopicBox.setToolTip('Number of topics to be displayed (10 by default).')
        self.numTopicBox.setValue(10)

        # Looking for some widget to use to change model types
        self.graphTypeBox = QComboBox()
        graphTypeList = ['Line', 'Bar', 'Pie']
        self.graphTypeBox.insertItems(0, graphTypeList)
        self.graphTypeBox.setToolTip('Choose what kind of graph the data should be displayed as.')

        # Testing Loading .gif widgets....
        # self.loadingLabel = QLabel()
        # self.loadingGif = QMovie('Loading_icon.gif')
        # self.loadingLabel.setMovie(self.loadingGif)
        # self.loadingGif.start()
        # self.loadingLabel.setVisible(True)

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
        #vBox1.addWidget(self.loadingLabel)

        mainLayout = QGridLayout()
        # mainLayout.addWidget(nameLabel, 0, 0)
        mainLayout.addLayout(vBox1, 0, 1)
        #mainLayout.addLayout(hLayout, 0, 1)
 
        self.setLayout(mainLayout)
        self.setWindowTitle('Next Top Model')
 
    def callMalletButton(self):
        print('GUI - Call Mallet button pressed.')
        mPath = str(self.malletLine.text())
        # print(mPath)

        print('GUI - Testing:  ' + mPath)
        if mPath == "":
            QMessageBox.information(self, 'Error',
                                    'No path found.  Please enter the Mallet Program.')
            return
        elif 'Mallet' not in mPath and 'mallet' not in mPath:
            QMessageBox.information(self, 'Error',
                                    'Mallet not found in path.  Please enter the Mallet Program.')
            return
        else:
            print('GUI - Valid path detected, calling mallet based on operating system.')
            QMessageBox.information(self, 'Mallet Called', 'Please wait as Mallet processes your input file.')

            if os.name == 'nt':
                # calls for Windows machines
                print('GUI - Windows - MalletCaller.py executing -- Please Wait.')
                call(['python', 'MalletCaller.py', mPath, str(self.numTopicBox.value())], shell=True)
                print('GUI - Windows - FileFilter.py executing -- Please Wait.')
                call(['python', 'FileFilter.py'], shell=True)
                print('GUI - Windows - TopicStocker.py executing -- Please Wait.')
                call(['python', 'TopicStocker.py', str(self.numTopicBox.value())], shell=True)
            elif os.name == 'posix':
                # *fixed* calls for Linux
                print('GUI - Linux - MalletCaller.py executing -- Please Wait.')
                call(['python3.5 MalletCaller.py ' + mPath + ' ' + str(self.numTopicBox.value())], shell=True)
                print('GUI - Linux - FileFilter.py executing -- Please Wait.')
                call(['python3.5 FileFilter.py'], shell=True)
                print('GUI - Linux - TopicStocker.py executing -- Please Wait.')
                call(['python3.5 TopicStocker.py ' + str(self.numTopicBox.value())], shell=True)
            else:
                print('GUI - Warning, Operating System is not supported.')

            # I thought this was appropriate because it takes a little while for everything to finish
            print('GUI - All Mallet modules done processing.')
            QMessageBox.information(self, 'Processing Completed', 'Mallet has finished processing.')
            return
    
    def callParseButton(self):
        print('GUI - Call Parser button pressed.')
        inputFile = self.inputLine.text()

        print('GUI - Testing:  ' + inputFile)
        if inputFile == "":
            QMessageBox.information(self, 'Error',
                                    'Please enter the Input file.')
            return
        elif '.xls' not in inputFile or '.xlsx' not in inputFile:
            QMessageBox.information(self, 'Error', 'Please enter a valid input file.')
            return
        else:
            print('GUI - Valid path detected, calling parser.')
            QMessageBox.information(self, 'Valid Input File',
                                    'Parsing %s for Mallet' % inputFile)

            #self.loadingLabel.setEnabled(True)

            if os.name == 'nt':
                # Working call for Windows machines
                # the one and the datelist arguments needed to be separated
                # hopefully this causes an error for Linux
                print('GUI - Windows - ExcelParser.py executing -- Please Wait.')
                call(['python', 'ExcelParser.py', inputFile, '1', '"3 4"'], shell=True)
            elif os.name == 'posix':
                # call for Linux machines
                print('GUI - Linux - ExcelParser.py executing -- Please Wait.')
                call(['python3.5 ExcelParser.py ' + inputFile + ' 1 "3 4"'], shell=True)
            else:
                print('GUI - Warning, Operating System is not supported.')

            # decided to steal this from Titus since it's a good idea
            #self.loadingLabel.setEnabled(False)
            print('GUI - Parser processing completed.')
            QMessageBox.information(self, 'Processing Completed', 'Parser has completed.')
            return

    def fileSearch(self):
        # QFileDialog.getOpenFileName probably gets us as close to a decent path + filename as we can get
        # But it requires some clever formatting to get it to a usable string
        print('GUI - File Search button pressed')
        fname = QFileDialog.getOpenFileName(self, 'Open file')

        fname1 = str(fname).split()
        # str(fname) returns ('/path/to/file', All Files (*)')
        # so str(fname).split() is used to get ('/path/to/file' by itself so it can  be parsed easier

        inputLen = len(fname1[0])               # we need to know how long the input is
        inputLen -= 2                                   # get rid of the last two characters ',
        inputFile = fname1[0][2:inputLen]    # strip off the first two characters ('

        # These print statements show exactly what the problem was and how it was progressively resolved
        #print(str(fname))
        #print(fname1[0])
        #print(inputfile)

        print('GUI - Testing:  ' + inputFile)
        # all my mallet stuff is lowercase but we'll have both, the actual program should be lowercase though
        if 'Mallet' in inputFile or 'mallet' in inputFile:
            print('GUI - Mallet input path detected, setting Mallet line.')
            self.malletLine.setText(inputFile)
            self.malletButton.setEnabled(True)
            return
        elif '.xls' in inputFile or '.xlsx' in inputFile:
            print('GUI - Excel input path detected, setting Excel line.')
            self.inputLine.setText(inputFile)
            self.parseButton.setEnabled(True)
            return
        else:
            QMessageBox.information(self, 'Error', 'Please enter a valid input file')
            return
        # self.inputLine.setText(fname)

    # This will be the function that displays the generated graphs
    # def showGraph(self):
        # return

# code below looks for inputdirectory in the program path location, if it is not found, the program makes one
ipDir = 'inputdirectory'
if not os.path.exists(ipDir):
    print('GUI - Creating Input Directory')
    os.makedirs(ipDir)      # Chris:  I'm pretty sure this will work just fine on Windows as well
else:
    print('GUI - Input Directory Found.')

if __name__ == '__main__':
    import sys
 
    app = QApplication(sys.argv)
 
    screen = Form()
    screen.show()
 
    sys.exit(app.exec_()) 

