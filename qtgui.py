from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
 
class Form(QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        
        inputlabel = QLabel("Input File Location:")
        self.inputline = QLineEdit("/Path/To/Input/File.xlsx")
        self.parse = QPushButton("Parse Input")
 
        malletlabel = QLabel("Mallet Location:")
        self.malletline = QLineEdit("/Path/To/Mallet")
        self.callmallet = QPushButton("Call Mallet")
        
        self.enhCheck = QCheckBox("View Enhancements")
        self.bugCheck = QCheckBox("View Bugs")
 
        buttonLayout1 = QVBoxLayout()
        buttonLayout1.addWidget(inputlabel)
        buttonLayout1.addWidget(self.inputline)
        buttonLayout1.addWidget(self.parse)
        buttonLayout1.addWidget(malletlabel)
        buttonLayout1.addWidget(self.malletline)
        buttonLayout1.addWidget(self.callmallet)
        buttonLayout1.addWidget(self.enhCheck)
        buttonLayout1.addWidget(self.bugCheck)
 
        self.callmallet.clicked.connect(self.callMalletButton)
        self.parse.clicked.connect(self.callParseButton)
 
        mainLayout = QGridLayout()
        # mainLayout.addWidget(nameLabel, 0, 0)
        mainLayout.addLayout(buttonLayout1, 0, 1)
 
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
