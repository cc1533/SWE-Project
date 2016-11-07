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
#       Fill in functions
#       Translate sevNum into user-friendly string
#
#
#####################################################################################################
#!/usr/bin/python
"""

from ggplot import *
from pandas import *
from Topics import *


class VisualModeler:

    def __init__(self):
        # just a placeholder atm
        self.__name = "Visual Modeling Class"

    @staticmethod
    def modelVolumeEnhView(enhTopics):
        counts = []
        topics = []
        topicNum = 0
        for topic in enhTopics:
            countSum = 0
            datesAndCounts = topic.getDatesAndCounts()
            for key, value in datesAndCounts:
                countSum += value
            topics.append(topicNum)
            counts.append(countSum)

        dF = DataFrame(data={'topics': topics, 'counts': counts})

        plot = ggplot(dF, aes(x='topics', weight='counts')) + geom_bar()
        return plot

    @staticmethod
    def modelDateView(enhTopic):
        datesAndCounts = enhTopic.getDatesAndCounts()
        dates = []
        counts = []
        for key, value in datesAndCounts:
            dates.append(key)
            counts.append(value)

        formattedDates = to_datetime(Series(dates))
        dF = DataFrame(data={'dates': formattedDates, 'reports': counts})
        plot = ggplot(dF, aes(x='dates', y='reports')) + geom_line()
        return plot

    @staticmethod
    def modelVolumeBugView(bugTopics):
        return None

    @staticmethod
    def modelMultiDateView(bugTopic):
        severityDatesAndCounts = bugTopic.getDatesAndCounts()

        sevs = []
        dates = []
        counts = []

        sevNum = 0
        for severity in severityDatesAndCounts:
            for key, value in severityDatesAndCounts[severity]:
                dates.append(key)
                counts.append(value)
                sevs.append(str(sevNum))
            sevNum += 1

        formattedDates = to_datetime(Series(dates))
        dF = DataFrame(data={'dates': formattedDates, 'reports': counts, 'severity': sevs})
        plot = ggplot(dF, aes(x='dates', y='reports', color='severity')) + geom_line()
        return plot

    @staticmethod
    def modelDividedView(bugTopic):
        return None
