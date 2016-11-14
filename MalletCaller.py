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
from subprocess import call
from sys import argv


# Sets MALLET_HOME environment variable, Windows only
if os.name == 'nt':
    os.environ['MALLET_HOME'] = "C:/mallet"

# making some more linux friendly changes
# malletPath will now be defined as an argument (since the GUI asks the user for it anyway)
malletPath = argv[1]
# malletPath = "C:/NextTopModel"
# input directory will be in whatever the current working directory is (i.e. wherever MalletCaller.py is)
inputPath = os.getcwd() + '/inputdirectory'
# inputPath = malletPath + "/inputdirectory"

numTopics = argv[2]
numIterations = "30"        # Chris:  is 30 just arbitrarily picked?  What's the significance?


class Mallet(object):
    
    def __init__(self, malletPath):
        
        self.malletExec = malletPath  # + "/bin/mallet"
    
    def importDir(self):
        
        output = "readyforinput.mallet"
        call(self.malletExec + " import-dir --input " + inputPath + " --keep-sequence --stoplist-file en.txt --output " + output, shell=True)
    
    def trainTopics(self):
        
        #inputFile = malletPath + "/readyforinput.mallet"
        inputFile = 'readyforinput.mallet'
        outputState = "output_state.gz"
        command = self.malletExec + " train-topics --input " + inputFile + " --num-topics " + numTopics + " --output-state " + outputState + " --num-iterations " + numIterations
        call(command, shell=True)

    def unzipOutput(self):

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


callmallet = Mallet(malletPath)
callmallet.importDir()
callmallet.trainTopics()
callmallet.unzipOutput()
