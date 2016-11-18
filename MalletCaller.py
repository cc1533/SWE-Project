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
    def __init__(self, malletPath, inputPath, numTopics, numIterations):
        print('MalletCaller - Initializing')

        # these paths need to be changed on Windows but not linux
        if os.name == 'nt':
            print('MalletCaller - Initializing Windows Paths')
            self.malletExec = malletPath.replace('/', '\\')
            self.inputPath = inputPath.replace('/', '\\')

        else:
            # else (on linux)
            self.malletExec = malletPath
            self.inputPath = inputPath

        self.numTopics = numTopics
        self.numIterations = numIterations
    
    def importDir(self):
        print('MalletCaller - Importing Directory for Mallet Processing')
        output = os.getcwd() + '/readyforinput.mallet'

        # command didn't work on Linux, modified to be linux friendly
        if os.name == 'nt':
            command = [self.malletExec, "import-dir", "--input", self.inputPath, "--keep-sequence", "--stoplist-file", "en.txt", "--output", output]
        else:
            command = [self.malletExec + ' import-dir --input ' + self.inputPath + ' --keep-sequence --stoplist-file en.txt --output ' + output]
        # print(command)
        run(command, shell=True, check=True)
    
    def trainTopics(self):
        print('MalletCaller - Training Mallet')

        inputPathLen = len(self.inputPath)
        inputPathLen -= 14

        # gets rid of .../'inputdirectory' so that the inputFile = .../readyforinput.mallet
        inputFile = self.inputPath[:inputPathLen] + 'readyforinput.mallet'
        outputState = "output_state.gz"
        
        # same issue as above, in importDir(), original command was not linux friendly
        if os.name == 'nt':
            command = [self.malletExec, "train-topics", "--input", inputFile, "--num-topics", str(self.numTopics), "--output-state", outputState, "--num-iterations", self.numIterations]
        else:
            command = [self.malletExec + ' train-topics --input ' + inputFile + ' --num-topics ' +  str(self.numTopics) + ' --output-state ' + outputState + ' --num-iterations ' + self.numIterations]
        # print(command)
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

    # input directory will be in whatever the current working directory is (i.e. wherever MalletCaller.py is)
    inputPath = os.getcwd() + '/inputdirectory'

    numIterations = "30"  # Chris:  is 30 just arbitrarily picked?  What's the significance?

    # print('MalletCaller - Mallet Path = ' + malletPath + '\n' + 'MalletCaller - Input Path = ' + inputPath + '\n' + 'MalletCaller - Number of Topics = ' + numTopics)

    callmallet = Mallet(malletPath, inputPath, numTopics, numIterations)
    callmallet.importDir()
    callmallet.trainTopics()
    callmallet.unzipOutput()
