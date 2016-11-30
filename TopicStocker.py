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
#                          - parse keyword & topic data from mallet output
#                          - parse keyword line location from filtered Title/Description column
#                          - parse date & category(bug/enhancement) data from excel(TXT)
#                          - utilize Topics.py in order to stock Topic objects with data
#
#####################################################################################################
#!/usr/bin/python
'''


import Topics
from sys import argv


class TopicStocker():

    def __init__(self):

        # list containing an enhancement topic object for each topic
        self.__enhTopics = []
        # list containing a bug topic object for each topic
        self.__bugTopics = []
        # 2D list containing lists for each enhancement topic's word list
        self.__enhWords = []
        # 3D list containing lists for each bug topic's severity's word list
        # 0:trivial, 1:minor, 2:normal, 3:major, 4:critical, 5:blocker
        self.__bugWords = []

        self.__numTopics = 0

        self.__TopWords = []
        self.__TopTopicWords = []

    def getEnhTopics(self):
        
        return self.__enhTopics

    def getBugTopics(self):
        
        return self.__bugTopics

    def getTopTopicWords(self):

        return self.__TopTopicWords

    def initializeTopics(self, numOfTopics):

        self.__numTopics = numOfTopics
        
        for i in range(int(self.__numTopics)):
            self.__enhTopics.append(Topics.EnhancementTopic())
            self.__bugTopics.append(Topics.BugTopic())

        self.__enhWords = [[] for x in range(int(self.__numTopics))]
        self.__bugWords = [[[] for x in range(6)] for x in range(int(self.__numTopics))]

        self.__TopWords = [{} for x in range(int(self.__numTopics))]

    def stockTopics(self):

        # file with keywords & mallet topics
        with open("output_state", "r") as keyFile:
            keys = keyFile.readlines()
            
        # file with keywords in lines & order from excel doc
        with open("FILTERED.txt", "r") as linedKeyFile:
            linedKeys = linedKeyFile.readlines()
            
        # file with excel text table (has dates & types)
        with open("EXCEL.txt", "r") as dateTypeFile:
            datesTypes = dateTypeFile.readlines()


        # line index of output_state file
        keyline = 3
        # line index of FILTERED.txt file
        lineKeyIndex = 0
        # line index of EXCEL.txt file
        dateTypeLine = 1
        # number of keys seen (comparable with index of same word in FILTERED.txt)
        keyIndex = 0
        # number of words in line from FILTERED.txt file
        keyIndexMax = 0


        # this section adds & increments the dates for each topic object
        # it also stocks each topics wordlist for later assignment
        keyIndexMax += len(linedKeys[lineKeyIndex].split())

        while (keyline < len(keys)):
            
            while (keyIndex >= keyIndexMax - 1):
                lineKeyIndex += 1
                keyIndexMax += len(linedKeys[lineKeyIndex].split())
                dateTypeLine += 1

            keyword = keys[keyline].split()[4]

            # this is here becasue of some foreign characters found in the mallet output that are sometimes split
            # into 2 separate indices. the except puts these 2 indeces together
            try:
                topic = int(keys[keyline].split()[5])
            except:
                #this was just to see what the line looked like
                #print("["+ str(keys[keyline].split()) + "] line: " + str(keyline) + " exline: " + str(dateTypeLine))
                #quit()
                
                keyword = keys[keyline].split()[4] + keys[keyline].split()[5]
                topic = int(keys[keyline].split()[6])

            dateTemp = datesTypes[dateTypeLine].split('\t')[3]

            date = dateTemp[:(dateTemp.rfind('-'))]
            category = datesTypes[dateTypeLine].split('\t')[2]
            
            if (category == "enhancement"):
                self.__enhTopics[topic].incDateCount(date)
                if (keyword not in self.__enhWords[topic]):
                    self.__enhWords[topic].append(keyword)

            else:
                if (category == "trivial"):
                    if (keyword not in self.__bugWords[topic][0]):
                        self.__bugWords[topic][0].append(keyword)
                    self.__bugTopics[topic].incDateCount(category, date)


                elif (category == "minor"):
                    if (keyword not in self.__bugWords[topic][1]):
                        self.__bugWords[topic][1].append(keyword)
                    self.__bugTopics[topic].incDateCount(category, date)

                elif (category == "normal"):
                    if (keyword not in self.__bugWords[topic][2]):
                        self.__bugWords[topic][2].append(keyword)
                    self.__bugTopics[topic].incDateCount(category, date)

                elif (category == "major"):
                    if (keyword not in self.__bugWords[topic][3]):
                        self.__bugWords[topic][3].append(keyword)
                    self.__bugTopics[topic].incDateCount(category, date)

                elif (category == "critical"):
                    if (keyword not in self.__bugWords[topic][4]):
                        self.__bugWords[topic][4].append(keyword)
                    self.__bugTopics[topic].incDateCount(category, date)

                elif (category == "blocker"):
                    if (keyword not in self.__bugWords[topic][5]):
                        self.__bugWords[topic][5].append(keyword)
                    self.__bugTopics[topic].incDateCount(category, date)

            if (keyword not in self.__TopWords[topic]):
                self.__TopWords[topic][keyword] = 1
            else:
                self.__TopWords[topic][keyword] += 1

            keyIndex += 1
            keyline += 1

        tempTopWords = self.__TopWords
        for x in range(int(self.__numTopics)):
            while True:
                maxWord = max(tempTopWords[x], key=lambda k: tempTopWords[x][k])
                if maxWord in self.__TopTopicWords:
                    tempTopWords[x].pop(maxWord)
                else:
                    lookAgain = False
                    for word in self.__TopTopicWords:
                        if maxWord in word or word in maxWord:
                            tempTopWords[x].pop(maxWord)
                            lookAgain = True
                    if not lookAgain:
                        break

            self.__TopTopicWords.append(maxWord)


        # this section sets the wordlist for each topic/severity etc...
        topic = 0
        severity = ["trivial", "minor", "normal", "major", "critical", "blocker"]
        while (topic < int(self.__numTopics)):
            self.__enhTopics[topic].setWords(self.__enhWords[topic])
            topic += 1

        topic = 0
        sev = 0
        while (topic < int(self.__numTopics)):
            sev = 0
            while (sev < len(self.__bugWords[topic])):
                self.__bugTopics[topic].setWords(severity[sev], self.__bugWords[topic][sev])
                sev += 1
            topic += 1


def main(numOfTopics):

    stockTopics = TopicStocker()
    stockTopics.initializeTopics(numOfTopics)
    stockTopics.stockTopics()
    return stockTopics
    # TEST
    """
    enhTopics = stockTopics.getEnhTopics()
    bugTopics = stockTopics.getBugTopics()

    i = 0
    for topic in enhTopics:
        print("EnhTopic " + str(i) + " 2003-09-22 date count: " + str(topic.getDateCount("2003-09-22")))
        print("EnhTopic " + str(i) + " 2007-11-16 date count: " + str(topic.getDateCount("2007-11-16")))
        print("EnhTopic " + str(i) + " 2004-10-23 date count: " + str(topic.getDateCount("2004-10-23")))
        print("EnhTopic " + str(i) + " 2003-09-22 date count: " + str(topic.getDateCount("2003-09-22")))
        print("")
        i += 1
    i = 0
    for topic in bugTopics:
        print("BugTopic " + str(i) + " normal 2003-09-22 date count: " + str(topic.getDateCount("normal","2003-09-22")))
        print("BugTopic " + str(i) + " normal 2007-11-16 date count: " + str(topic.getDateCount("normal","2007-11-16")))
        print("BugTopic " + str(i) + " normal 2004-10-23 date count: " + str(topic.getDateCount("normal","2004-10-23")))
        print("BugTopic " + str(i) + " normal 2003-09-22 date count: " + str(topic.getDateCount("normal","2003-09-22")))
        print("")
        i += 1
    """
    # TEST: END
