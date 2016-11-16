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
#                          - call mallet to perform topic modeling
#                          - unzips mallet output_state file
#
#                       This program assumes the following folders are in the same directory
#                          - inputdirectory
#
#####################################################################################################
#!/usr/bin/python
'''


import os
import gzip
from subprocess import run


class Mallet(object):
    def __init__(self, malletPath, binPath, inputPath, numTopics, numIterations):
        print('MalletCaller - Initializing')
        self.malletExec = malletPath.replace('/', '\\')
        self.binPath = binPath.replace('/', '\\')
        self.inputPath = inputPath
        self.numTopics = numTopics
        self.numIterations = numIterations
    
    def importDir(self):
        print('MalletCaller - Importing Directory for Mallet Processing')
        # <<<<<<< Updated upstream
        # output = "readyforinput.mallet"
        output = self.binPath + 'readyforinput.mallet'
        print(self.inputPath)
        print(self.malletExec)
        command = [self.malletExec, "import-dir", "--input", self.inputPath, "--keep-sequence", "--stoplist-file", "en.txt", "--output", output]
        #print(command)
        run(command, shell=True, check=True)
        '''
        =======
        output = "readyforinput.mallet"
        #inputPathLen = len(self.inputPath)
        #inputPathLen -= 15
        #output = self.inputPath + 'readyforinput.mallet'
        call(self.malletExec + " import-dir --input " + self.inputPath + " --keep-sequence --stoplist-file en.txt --output " + output, shell=True)
        >>>>>>> Stashed changes
        '''
    
    def trainTopics(self):
        print('MalletCaller - Training Mallet')
        # inputFile = malletPath + "/readyforinput.mallet"
        inputPathLen = len(self.inputPath)
        inputPathLen -= 14
        # homePath = self.inputPath[:inputPathLen]
        inputFile = self.inputPath[:inputPathLen] + 'readyforinput.mallet'
        outputState = "output_state.gz"
        command = [self.malletExec, "train-topics", "--input", inputFile, "--num-topics", str(self.numTopics), "--output-state", outputState, "--num-iterations", self.numIterations]
        #print(command)
        run(command, shell=True, check=True)

    def unzipOutput(self):
        print('MalletCaller - Unzipping and formatting output')
        zipped = gzip.open("output_state.gz", "r")
        unzipped = open("output_state", "w")
        content = zipped.readlines()

        for line in content:
            
            while '\\n\'' in str(line):
                line = str(line).replace('\\n\'', "")
            while '\\n\"' in str(line):
                line = str(line).replace('\\n\"', "")
            while '\\r' in str(line):
                line = str(line).replace('\\r', "")
            while 'b\'' in str(line):
                line = str(line).replace('b\'', "")
            while 'b\"' in str(line):
                line = str(line).replace('b\"', "")
                
            unzipped.write(str(line))
            unzipped.write('\n')
            
        zipped.close()


def main(malletPath, numTopics):
    # Sets MALLET_HOME environment variable, Windows only
    if os.name == 'nt':
        os.environ['MALLET_HOME'] = "C:/mallet"

    # making some more linux friendly changes
    # malletPath will now be defined as an argument (since the GUI asks the user for it anyway)
    malletPathLen = len(malletPath)
    malletPathLen -= 6  # path usually ends with .../bin/mallet so this just cuts off the 'mallet' at the end
    binPath = malletPath[:malletPathLen]
    # malletPath = "C:/NextTopModel"
    # input directory will be in whatever the current working directory is (i.e. wherever MalletCaller.py is)
    inputPath = os.getcwd() + '/inputdirectory'
    # inputPath = malletPath + "/inputdirectory"

    numIterations = "30"  # Chris:  is 30 just arbitrarily picked?  What's the significance?

    # print('MalletCaller - Mallet Path = ' + malletPath + '\n' + 'MalletCaller - Input Path = ' + inputPath + '\n' + 'MalletCaller - Number of Topics = ' + numTopics)

    callmallet = Mallet(malletPath, binPath, inputPath, numTopics, numIterations)
    callmallet.importDir()
    callmallet.trainTopics()
    callmallet.unzipOutput()
