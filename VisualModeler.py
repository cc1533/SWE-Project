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
#
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

    def modelVolumeEnhView(self, enhTopics):
        return None

    def modelDateView(self, enhTopic):
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

    def modelVolumeBugView(self, bugTopics):
        return None

    def modelMultiDateView(self, bugTopic):
        return None

    def modelDividedView(self, bugTopic):
        return None
