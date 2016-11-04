from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
 
class Form(QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        
        inputlabel = QLabel("Input File Location:")
        self.inputline = QLineEdit("/Path/To/Input/File.xlsx")
        self.inputSearch = QPushButton("...")
        self.parse = QPushButton("Parse Input")
 
        malletlabel = QLabel("Mallet Location:")
        self.malletline = QLineEdit("/Path/To/Mallet")
        self.malletSearch = QPushButton("...")
        self.callmallet = QPushButton("Call Mallet")
        
        self.enhCheck = QCheckBox("View Enhancements")
        self.bugCheck = QCheckBox("View Bugs")
 
        vLayout = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        
        vLayout.addWidget(inputlabel)
        hbox1.addWidget(self.inputline)
        hbox1.addWidget(self.inputSearch)
        vLayout.addLayout(hbox1)
        vLayout.addWidget(self.parse)
        
        vLayout.addWidget(malletlabel)
        hbox2.addWidget(self.malletline)
        hbox2.addWidget(self.malletSearch)
        vLayout.addLayout(hbox2)
        vLayout.addWidget(self.callmallet)
        vLayout.addWidget(self.enhCheck)
        vLayout.addWidget(self.bugCheck)
 
        self.callmallet.clicked.connect(self.callMalletButton)
        self.parse.clicked.connect(self.callParseButton)
 
        mainLayout = QGridLayout()
        # mainLayout.addWidget(nameLabel, 0, 0)
        mainLayout.addLayout(vLayout, 0, 1)
        #mainLayout.addLayout(hLayout, 0, 1)
 
        self.setLayout(mainLayout)
        self.setWindowTitle("Next Top Model")
 
    def callMalletButton(self):
        name = self.malletLine.text()
 
        if name == "":
            QMessageBox.information(self, "Empty Field",
                                    "Please enter the Mallet Program.")
            return
        else:
            QMessageBox.information(self, "Success!",
                                    "Hello %s!" % name)
            return
    
    def callParseButton(self):
        inputFile = self.inputline.text()
 
        if inputFile == "":
            QMessageBox.information(self, "Empty Field",
                                    "Please enter the Mallet Program.")
            return
        else:
            QMessageBox.information(self, "Success!",
                                    "Hello %s!" % inputFile)
            return
    
 
if __name__ == '__main__':
    import sys
 
    app = QApplication(sys.argv)
 
    screen = Form()
    screen.show()
 
    sys.exit(app.exec_()) 
