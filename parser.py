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
#	Other stuff here...
#
#
#####################################################################################################
#	Program info:
#			- This program will parse the .xlsx to a plain text (.txt) file
#
#####################################################################################################

#!/usr/bin/python

import platform		# needed to tell what OS the host system is running
import sys		# get args from commandline
import openpyxl		# for .xlsx parsing
import os		# determines pathway
import getopt		# argument parsing

def parser():
	#print 'Host System:  ', platform.system()
	hostSystem = platform.system()
	#print 'Current Dir Location:  ', os.path.abspath(__file__)
	currPW = os.path.abspath(__file__)
	# Python will need to be passed input filename, input file pathway
	#print 'Number of arguments:', len(sys.argv), 'arguments.'
	argLen = len(sys.argv)
	#print 'Argument List:', str(sys.argv)
	argList = str(sys.argv)

	# call should be something like "python parser.py [/path/to/file/] [inputFileName.xlsx]"
	if argLen < 3:
		print "**ERROR** Parser Expects 3 Arguments **EXITING SAFELY**"
		exit()

	# If it gets to here, there's the correct # of arguments
	print "Checking Args"

	inputfile = ''
	inputpath = ''
	outputfile = 'malletInput.txt'

	try:
		

	#book = xlrd.open_workbook(
	# Output file will be "malletInput.txt"

parser()

