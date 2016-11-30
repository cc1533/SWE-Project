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
    def modelVolumeEnhView(enhTopics, topicWordList):
        counts = []
        topics = []
        topicNum = 0
        for topic in enhTopics:
            countSum = 0
            datesAndCounts = topic.getDatesAndCounts()
            for key, value in datesAndCounts.items():
                countSum += value
            topics.append(topicWordList[topicNum])
            counts.append(countSum)
            topicNum += 1

        dF = DataFrame(data={'topics': topics, 'counts': counts})

        plot = ggplot(dF, aes(x='topics', weight='counts')) + \
               geom_bar() + \
               ggtitle("Total Counts for each Topic") + \
               xlab("Topics") + \
               ylab("Total Count")
        return plot

    @staticmethod
    def modelDateView(enhTopic, topicWord):
        datesAndCounts = enhTopic.getDatesAndCounts()
        dates = []
        counts = []
        for key, value in datesAndCounts.items():
            dates.append(key)
            counts.append(value)

        formattedDates = to_datetime(Series(dates))
        dF = DataFrame(data={'dates': formattedDates, 'reports': counts})
        plot = ggplot(dF, aes(x='dates', y='reports')) + \
               geom_line() + \
               ggtitle("Total Counts By Date For " + topicWord) + \
               xlab("Date") + \
               ylab("Total Count")
        return plot

    @staticmethod
    def modelVolumeBugView(bugTopics, topicWordList):
        topics = []
        severities = [[], [], [], [], [], []]
        topicNum = 0
        severity = ["trivial", "minor", "normal", "major", "critical", "blocker"]
        for topic in bugTopics:
            for severityNum in range(6):
                countSum = 0
                severityDates = topic.getDates(severity[severityNum])
                for key in severityDates:
                    countSum += topic.getDateCount(severity[severityNum], key)
                severities[severityNum].append(countSum)
            topics.append(topicWordList[topicNum])
            topicNum += 1

        dF = DataFrame(data={'topics': topics, 'trivial': severities[0], 'minor': severities[1], 'normal': severities[2], 'major': severities[3], 'critical': severities[4], 'blocker': severities[5]})
        data = melt(dF, id_vars='topics')

        plot = ggplot(data, aes(x='topics', weight='value', fill='variable')) + \
               geom_bar(stat='identity') + \
               ggtitle("Total Counts By Severity For Topics") + \
               xlab("Topics") + \
               ylab("Counts")
        return plot

    @staticmethod
    def modelMultiDateView(bugTopic, topicWord):
        sevs = []
        dates = []
        counts = []
        severity = ["trivial", "minor", "normal", "major", "critical", "blocker"]
        for severityNum in range(6):
            severityDates = bugTopic.getDates(severity[severityNum])
            for key in severityDates:
                count = bugTopic.getDateCount(severity[severityNum], key)
                dates.append(key)
                counts.append(count)
                sevs.append(severity[severityNum])

        formattedDates = to_datetime(Series(dates))
        dF = DataFrame(data={'dates': formattedDates, 'reports': counts, 'severity': sevs})
        plot = ggplot(dF, aes(x='dates', y='reports', color='severity')) + \
               geom_line() + \
               ggtitle("Total Counts By Date For " + topicWord) + \
               xlab("Date") + \
               ylab("Total Count")
        return plot

    @staticmethod
    def modelDividedView(bugTopic, topicWord):
        severities = []
        counts = []
        severity = ["trivial", "minor", "normal", "major", "critical", "blocker"]
        for severityNum in range(6):
            countSum = 0
            dates = bugTopic.getDates(severity[severityNum])
            for key in dates:
                countSum += bugTopic.getDateCount(severity[severityNum], key)
            severities.append(severity[severityNum])
            counts.append(countSum)

        dF = DataFrame(data={'severities': severities, 'counts': counts})

        plot = ggplot(dF, aes(x='severities', weight='counts')) + \
               geom_bar() + \
               ggtitle("Total Counts By Severity For " + topicWord) + \
               xlab("Severity") + \
               ylab("Total Count")
        return plot
