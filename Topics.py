"""
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
#
#
#
#
#####################################################################################################
#!/usr/bin/python
"""


class EnhancementTopic:

    def __init__(self):
        self.__wordList = []
        self.__dateCounts = {}

    def setWords(self, wordList):
        self.__wordList = wordList

    def incDateCount(self, date):
        if (date in self.__dateCounts):
            self.__dateCounts[date] += 1
        else:
            self.__dateCounts[date] = 1

    def getDateCount(self, date):
        if (date in self.__dateCounts):
            return self.__dateCounts[date]
        else:
            return 0

    def getDatesAndCounts(self):
        return self.__dateCounts


class BugTopic:

    def __init__(self):
        self.__bugDateCounts = {}
        self.__severityWordLists = {}

    def setWords(self, severity, wordList):
        self.__severityWordLists[severity] = wordList

    def incDateCount(self, severity, date):
        if (severity in self.__bugDateCounts):
            if (date in self.__bugDateCounts[severity]):
                self.__bugDateCounts[severity][date] += 1
            else:
                self.__bugDateCounts[severity][date] = 1
        else:
            self.__bugDateCounts[severity] = {}
            self.__bugDateCounts[severity][date] = 1

    def getDateCount(self, severity, date):
        if (date in self.__bugDateCounts[severity]):
            return self.__bugDateCounts[severity][date]
        else:
            return 0

    def getDates(self, severity):
        return self.__bugDateCounts[severity].keys()
