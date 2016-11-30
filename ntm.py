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
#       Functional:
#	1.  Have all functional requirements been implemented?
#
#	Non-Functional:
#	1.  Testing on Windows/Linux, whomever has all of the python libraries installed
#	2.  Add Session functionality via menubar options
#
#####################################################################################################
#  Program info:
# 	- This is the GUI that the user will interface with and drive the program.
#
#####################################################################################################
# !/usr/bin/python

# Import all the modules/libraries we're using
import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# import the other modules we wrote for this program
import VisualModeler
import TopicStocker
import FileFilter
import MalletCaller
import ExcelParser

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
        self.__topics = None

    def initUI(self):
        # setGeometry(self, ax, ay, aw, ah) -> x, y, width, height
        x = 500
        y = 200
        self.setGeometry(x, y, x, y)

        # Create layout boxes (makes things line up nicely)
        vertBox = QVBoxLayout()
        hInputBox = QHBoxLayout()
        hNumTopicBox = QHBoxLayout()
        hMalletBox = QHBoxLayout()
        hTopicBox = QHBoxLayout()

        # Create menu bar actions (not the bar itself yet)
        openAction = QAction('Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open Saved Session')
        #openAction.triggered.connect(self.openSession)
        closeAction = QAction('Close', self)
        closeAction.setShortcut('Ctrl+Q')
        closeAction.setStatusTip('Close Session Without Saving')
        #closeAction.triggered.connect(self.closeSession)
        saveAction = QAction('Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save Session')
        # saveAction.triggered.connect(self.saveSession)

        # Couldn't get menubar functional in time, commented out for now
        '''
        # Create menubar and add actions to the bar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(closeAction)
        fileMenu.addAction(saveAction)
        '''

        # Create input file label, text line, search button and the parser button
        inputLabel = QLabel('Input Excel File Location:')
        self.inputLine = QLineEdit('/Path/To/Input/File')
        self.inputLine.setReadOnly(True)
        self.inputLine.setToolTip('This is the path to the input file Mallet should process.')
        self.inputSearch = QPushButton("...")
        self.inputSearch.setToolTip('Find the file Mallet should process.')
        self.inputSearch.clicked.connect(self.fileSearch)
        # Add the first set of widgets to the window (input file stuff)
        vertBox.addWidget(inputLabel)
        hInputBox.addWidget(self.inputLine)
        hInputBox.addWidget(self.inputSearch)
        vertBox.addLayout(hInputBox)

        # Create spin box widget to get the # of desired topics displayed in the model
        defaultNumTopics = 5
        numTopicLabel = QLabel('Number of Topics:  ')
        self.numTopicBox = QSpinBox()
        self.numTopicBox.setRange(1, 10)  # Arbitrarily picked 20, idk what the max should be
        self.numTopicBox.setToolTip('Number of topics to be displayed (5 by default).')
        self.numTopicBox.setValue(defaultNumTopics)
        self.numTopicBox.valueChanged.connect(self.disableDisplayModel)
        # Add # of topics box
        hNumTopicBox.addWidget(numTopicLabel)
        hNumTopicBox.addWidget(self.numTopicBox)
        vertBox.addLayout(hNumTopicBox)

        # Create mallet label, text line, search button and call mallet button
        malletLabel = QLabel('Mallet Location:')
        self.malletLine = QLineEdit('/Path/To/Mallet/Program')
        self.malletLine.setReadOnly(True)
        self.malletLine.setToolTip('This is the path to where the Mallet program is located.')
        self.malletSearch = QPushButton("...")
        self.malletSearch.setToolTip('Find the Mallet program.')
        self.malletSearch.clicked.connect(self.fileSearch)
        self.malletSearch.setEnabled(False)
        # Add the second set of widgets to the window (mallet stuff)
        vertBox.addWidget(malletLabel)
        hMalletBox.addWidget(self.malletLine)
        hMalletBox.addWidget(self.malletSearch)
        vertBox.addLayout(hMalletBox)

        # Create Run button to parse input file and call mallet
        self.runButton = QPushButton('Execute')
        self.runButton.setToolTip('Parses Excel Input File and Calls Mallet')
        self.runButton.clicked.connect(self.exeqt)
        self.runButton.setEnabled(False)
        # Add run button to window
        vertBox.addWidget(self.runButton)

        # Create check boxes, these will be used later
        """
        self.enhRadio = QRadioButton('View Enhancements')
        self.enhRadio.setChecked(True)
        self.enhRadio.setToolTip('Show Enhancements?')
        self.bugRadio = QRadioButton('View Bugs')
        self.bugRadio.setChecked(False)
        self.bugRadio.setToolTip('Show Bugs?')
        # Add checkboxes and other widgets to window
        hRadioBox.addWidget(self.enhRadio)
        hRadioBox.addWidget(self.bugRadio)
        vertBox.addLayout(hRadioBox)
        """
        # Looking for some widget to use to change model types
        modelLabel = QLabel("Pick a Model:")
        self.graphTypeBox = QComboBox()
        graphTypeList = ['All Enhancements', 'Dates of Enhancements', 'All Bugs', 'Multi Date View of Bug', 'Date Divided View of Bug']
        self.graphTypeBox.insertItems(0, graphTypeList)
        self.graphTypeBox.setToolTip('Choose what kind of graph the data should be displayed as.')
        self.graphTypeBox.currentIndexChanged.connect(self.enableTopicBox)

        # Add graphTypeBox to window
        vertBox.addWidget(modelLabel)
        vertBox.addWidget(self.graphTypeBox)

        # Create Topic box
        topicLabel = QLabel("Topics: ")
        self.graphTopicBox = QComboBox()
        graphTopicList = []
        for num in range(1, defaultNumTopics+1):
            graphTopicList.append("Topic " + str(num))
        self.graphTopicBox.insertItems(0, graphTopicList)
        self.graphTopicBox.setToolTip('Choose which topic for graph')
        self.graphTopicBox.setEnabled(False)

        hTopicBox.addWidget(topicLabel)
        hTopicBox.addWidget(self.graphTopicBox, 1)
        vertBox.addLayout(hTopicBox)

        # Add seperate button to display models
        self.displayModelButton = QPushButton('Display Model')
        self.displayModelButton.setToolTip('Generate Models to be displayed')
        self.displayModelButton.clicked.connect(self.displayModels)
        self.displayModelButton.setEnabled(False)
        # Add display model button to window
        vertBox.addWidget(self.displayModelButton)

        mainLayout = QGridLayout()
        mainLayout.addLayout(vertBox, 0, 1)
        centWidget = QWidget()
        centWidget.setLayout(mainLayout)
        self.setCentralWidget(centWidget)

        self.setWindowTitle('Next Top Model')
        self.show()

    def enableTopicBox(self):
        graphType = self.graphTypeBox.currentText()
        if graphType == 'All Enhancements' or graphType == 'All Bugs':
            self.graphTopicBox.setEnabled(False)
        else:
            self.graphTopicBox.setEnabled(True)

    def updateTopicBox(self):
        try:
            self.graphTopicBox.clear()
            self.graphTopicBox.insertItems(0, self.__topics.getTopTopicWords())
            self.displayModelButton.setEnabled(False)
        except Exception:
            pass

    def disableDisplayModel(self):
        try:
            self.displayModelButton.setEnabled(False)
        except Exception:
            pass

    def exeqt(self):		# "exeqt" = "execute", a pun because we're using PyQt (Py-cute)
        print('GUI - Run button pressed.')
        malletPath = str(self.malletLine.text())
        inputFilePath = str(self.inputLine.text())

        print('GUI - Testing Mallet Path...')
        # checks for valid mallet path first
        if malletPath == '':
            QMessageBox.information(self, 'Error', 'No path found.  Please enter the Mallet Program.')
            return
        elif 'mallet' not in malletPath:
            QMessageBox.information(self, 'Error', 'Mallet not found in path.  Please enter the Mallet Program.')
            return
        else:
            print('GUI - Valid mallet path found, testing input file path.')

            # if the mallet path is valid, check input file path
            if inputFilePath == '':
                QMessageBox.information(self, 'Error', 'No path found.  Please enter the input file path.')
                return

            elif '.xls' not in inputFilePath and '.xlsx' not in inputFilePath:
                QMessageBox.information(self, 'Error', 'Valid Excel File not found.  Please enter a valid input file.')
                return

            else:
                # if both paths are valid, go ahead and run the modules
                print('GUI - Input File and Mallet paths are valid, running...')

                # Call Parser
                print('GUI - ExcelParser.py executing -- Please Wait.')
                ExcelParser.main(inputFilePath, 1, ["3", "4"])

                # Call MalletCaller.py
                print('GUI - MalletCaller.py executing -- Please Wait.')
                MalletCaller.main(malletPath, self.numTopicBox.value())

                # Call FileFilter.py
                print('GUI - FileFilter.py executing -- Please Wait.')
                FileFilter.main()

                # Call TopicStocker.py
                print('GUI - TopicStocker.py executing -- Please Wait.')
                self.__topics = TopicStocker.main(self.numTopicBox.value())
                self.updateTopicBox()

                print('GUI - All Mallet modules done processing.')
                QMessageBox.information(self, 'Processing Completed', 'Mallet modules have finished processing.')

                self.displayModelButton.setEnabled(True)

    def fileSearch(self):
        print('GUI - File Search button pressed')
        fname = QFileDialog.getOpenFileName(self, 'Open file')

        fname1 = str(fname).split()

        inputLen = len(fname1[0])					# we need to know how long the input is
        inputLen -= 2								# get rid of the last two characters ',
        inputFile = fname1[0][2:inputLen]			# strip off the first two characters ('

        print('GUI - Testing:  ' + inputFile)
        # Test to see if what the user gave as input was for the mallet program or the excel file
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

    def displayModels(self):
        # Call the VisualModeler.py
        print('GUI - VisualModeler.py executing -- Please Wait.')
        VisualModel = VisualModeler.VisualModeler()
        graphType = self.graphTypeBox.currentText()
        # Find the arrays of topics
        enhTopics = self.__topics.getEnhTopics()
        bugTopics = self.__topics.getBugTopics()

        # 'All Enhancements', 'Dates of Enhancements'
        # 'All Bugs', 'Multi Date View of Bug', 'Date Divided View of Bug'

        topicWords = self.__topics.getTopTopicWords()
        topicIndex = self.graphTopicBox.currentIndex()

        if graphType == 'All Enhancements':
            plot = VisualModel.modelVolumeEnhView(enhTopics, topicWords)
            print(plot)

        elif graphType == 'Dates of Enhancements':
            # When the user specifies the enhancement they want, pass that topic to the modeler
            enhTopic = enhTopics[topicIndex]
            plot = VisualModel.modelDateView(enhTopic, topicWords[topicIndex])
            print(plot)

        elif graphType == 'All Bugs':
            plot = VisualModel.modelVolumeBugView(bugTopics, topicWords)
            print(plot)

        elif graphType == 'Multi Date View of Bug':
            # When the user specifies the bug they want, pass that topic to the modeler
            bugTopic = bugTopics[topicIndex]
            plot = VisualModel.modelMultiDateView(bugTopic, topicWords[topicIndex])
            print(plot)

        elif graphType == 'Date Divided View of Bug':
            # When the user specifies the bug they want, pass that topic to the modeler
            bugTopic = bugTopics[topicIndex]
            plot = VisualModel.modelDividedView(bugTopic, topicWords[topicIndex])
            print(plot)

        """
        if self.enhRadio.isChecked():
            # Enhancements. one of: modelVolumeEnhView or modelDateView


        elif self.bugRadio.isChecked():
            # Bugs. one of: modelVolumeBugView, modelMultiDateView, modelDividedView
        """

    # placeholders for what would've been the code to add function to the menubar options
    '''
    def openSession(self):
        # This is where the code for the open session action of the menubar will be

    def closeSession(self):
        # This is where the code for the close session action of the menubar will be

    def saveSession(self):
        # This is where the code for the save session action of the menubar will be
    '''

def main():
    app = QApplication(sys.argv)
    gui = MainWindow()
    sys.exit(app.exec_())

# code below looks for inputdirectory in the program path location, if it is not found, the program makes one
ipDir = 'inputdirectory'
if not os.path.exists(ipDir):
    print('GUI - No Input Directory Found, Creating Input Directory')
    os.makedirs(ipDir)
else:
    print('GUI - Input Directory Found.')

if __name__ == '__main__':
    main()
