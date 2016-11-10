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


def initializeTopics(quantity):

    enhancementTopics = []
    bugTopics = []

    for i in range(quantity):
        enhancementTopics.append(Topics.EnhancementTopic())
        bugTopics.append(Topics.BugTopic())

    return enhancementTopics, bugTopics

def getNumberOfTopics():
    return int(argv[1])


# keys - file with keywords & mallet topics
# linedKeys - file with keywords in lines & order from excel doc
# datesTypes - excel text file; has dates and types

keyFile = open("output_state", "r")
linedKeyFile = open("FILTERED.txt", "r")
dateTypeFile = open("EXCEL.txt", "r")

keys = keyFile.readlines()
linedKeys = linedKeyFile.readlines()
datesTypes = dateTypeFile.readlines()

keyFile.close()
linedKeyFile.close()
dateTypeFile.close()


# keyline - line index of output_state file
#lineKeyIndex - line index of FILTERED.txt file
# dateTypeLine - line index of EXCEL.txt file
# keyIndex - number of keys seen (comparable with index of same word in FILTERED.txt)
# keyIndexMax - number of words in line from FILTERED.txt file

keyline = 3
lineKeyIndex = 0
dateTypeLine = 1
keyIndex = 0
keyIndexMax = 0


# enhTopics: list containing an enhancement topic object for each topic
# bugTopics: list containing a bug topic object for each topic
# enhWords: 2D list containing lists for each enhancement topic's word list
# bugWords: 3D list containing lists for each bug topic's severity's word list
#            - each list contains 6 lists; one for each severity
#               - 0 - TRIVIAL
#               - 1 - MINOR
#               - 2 - NORMAL
#               - 3 - MAJOR
#               - 4 - CRITICAL
#               - 5 - BLOCKER

numberOfTopics = getNumberOfTopics()
enhTopics, bugTopics = initializeTopics(numberOfTopics)

enhWords = [[] for x in range(numberOfTopics)]
bugWords = [[[] for x in range(6)] for x in range(numberOfTopics)]


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
        #print("["+ str(keys[keyline].split()) + "] line: " + str(keyline) + " exline: " + str(dateTypeLine))
        #quit()
        
        keyword = keys[keyline].split()[4] + keys[keyline].split()[5]
        topic = int(keys[keyline].split()[6])

    date = datesTypes[dateTypeLine].split('\t')[3]
    category = datesTypes[dateTypeLine].split('\t')[2]
    
    if (category == "enhancement"):
        enhTopics[topic].incDateCount(date)
        if (keyword not in enhWords[topic]):
            enhWords[topic].append(keyword)

    else:
        bugTopics[topic].incDateCount(category, date)

        if (category == "trivial"):
            if (keyword not in bugWords[topic][0]):
                bugWords[topic][0].append(keyword)
                
        elif (category == "minor"):
            if (keyword not in bugWords[topic][1]):
                bugWords[topic][1].append(keyword)
                
        elif (category == "normal"):
            if (keyword not in bugWords[topic][2]):
                bugWords[topic][2].append(keyword)
                
        elif (category == "major"):
            if (keyword not in bugWords[topic][3]):
                bugWords[topic][3].append(keyword)
                
        elif (category == "critical"):
            if (keyword not in bugWords[topic][4]):
                bugWords[topic][4].append(keyword)
                
        elif (category == "blocker"):
            if (keyword not in bugWords[topic][5]):
                bugWords[topic][5].append(keyword)

    keyIndex += 1
    keyline += 1


topic = 0
sev = 0
severity = ["trivial", "minor", "normal", "major", "critical", "blocker"]
while (topic < numberOfTopics):
    enhTopics[topic].setWords(enhWords[topic])
    topic += 1

topic = 0
while (topic < numberOfTopics):
    sev = 0
    while (sev < len(bugWords[topic])):
        bugTopics[topic].setWords( severity[sev], bugWords[topic][sev] )
        sev += 1
    topic += 1
      
# TEST
"""
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
