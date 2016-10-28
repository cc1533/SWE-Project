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
#
#
#
#
#####################################################################################################
#   TODO:
#       Fill in functions
#
#
#
#####################################################################################################
#!/usr/bin/python
'''


class EnhancementTopic:

    def __init__(self):
        self.__wordList = []
        self.__dateCounts = {}

    def setWords(self, wordList):
        self.__wordList = wordList

    def incDateCount(self, date):
        if self.__dateCounts[date]:
            self.__dateCounts[date] += 1
        else:
            self.__dateCounts[date] = 1

    def getDateCount(self, date):
        return self.__dateCounts[date]


class BugTopic:

    def __init__(self):
        self.__bugDateCounts = {}
        self.__severityWordLists = {}

    def setWords(self, severity, wordList):
        self.__severityWordLists[severity] = wordList
        self.__bugDateCounts[severity] = {}

    def incDateCount(self, severity, date):
        if self.__bugDateCounts[severity][date]:
            self.__bugDateCounts[severity][date] += 1
        else:
            self.__bugDateCounts[severity][date] = 1

    def getDateCount(self, severity, date):
        return self.__bugDateCounts[severity][date]
