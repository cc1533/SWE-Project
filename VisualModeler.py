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
            topicNum += 1

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
        topics = []
        severities = []
        topicNum = 0
        for topic in bugTopics:
            for severity in range(6):
                countSum = 0
                datesAndCounts = topic.getDatesAndCounts(severity)
                severities[severity] = []
                for key, value in datesAndCounts:
                    countSum += value
                topics.append(topicNum)
                severities[severity].append(countSum)

        dF = DataFrame(data={'topics': topics, 's0': severities[0], 's1': severities[1], 's2': severities[2], 's3': severities[3], 's4': severities[4], 's5': severities[5]})
        data = melt(dF, id_vars='topics')

        plot = ggplot(data, aes(x='topics', weight='value', fill='variable')) + geom_bar(stat='identity')
        return plot

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
        severities = []
        counts = []
        for severity in range(6):
            countSum = 0
            datesAndCounts = bugTopic.getDatesAndCounts(severity)
            for key, value in datesAndCounts:
                countSum += value
            severities.append(severity)
            counts.append(countSum)

        dF = DataFrame(data={'severities': severities, 'counts': counts})

        plot = ggplot(dF, aes(x='severities', weight='counts')) + geom_bar()
        return plot
