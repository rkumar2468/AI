__author__ = 'sri'

import os, sys

class readInputFile:

    def __init__(self, filename):
        self.file = filename
        self.mailCnt = 0
        self.mailList = {}
        self.mailWordFreq = {}
        self.spamCnt = 0
        self.hamCnt = 0
        self.spamWordsSet = set()
        self.hamWordsSet = set()
        self.commonWords = set()
        self.uniqueSpamWords = {}
        self.uniqueHamWords = {}
        self.spamDict = {}
        self.hamDict = {}
        self.fileContents = {}

    def generateListsFromInputFile(self):
        if not os.path.exists(self.file):
            print "Error: The file "+self.file+" does not exists.\n"
            sys.exit(-1)
        f = open(self.file, 'r')
        count = 0
        for line in f:
            self.fileContents[count] = line
            count += 1
        self.mailCnt = count
        f.close()
        self.generateLists()

    def generateLists(self):
        for key in self.fileContents.keys():
            line = self.fileContents[key]
            line = line.strip(' ')
            line = line.strip('\n')

            self.mailCnt += 1
            lineList = line.split(' ')
            length = len(lineList)

            if lineList[1] == 'spam':
                self.spamCnt += 1
                for idx in range(2,length-1,2):
                    val = lineList[idx]
                    if val in self.spamDict.keys():
                        self.spamDict[val] += 1
                    else:
                        self.spamDict[val] = 1
                # sys.exit(-1)
                # for i in range(2, length-1, 2):
                #     self.spamWordsSet.add((lineList[i]))
                #
                #     if lineList[i] in self.spamDict.keys():
                #         self.spamDict[lineList[i]].append(lineList[i+1])
                #     else:
                #         self.spamDict[lineList[i]] = [lineList[i+1]]
            else:
                self.hamCnt += 1
                for idx in range(2,length-1,2):
                    val = lineList[idx]
                    if val in self.hamDict.keys():
                        self.hamDict[val] += 1
                    else:
                        self.hamDict[val] = 1
                # for i in range(2, length-1, 2):
                #     self.hamWordsSet.add(lineList[i])
                #
                # if lineList[i] in self.hamDict.keys():
                #         self.hamDict[lineList[i]].append(lineList[i+1])
                # else:
                #         self.hamDict[lineList[i]] = [lineList[i+1]]

            # self.commonWords = self.spamWordsSet.intersection(self.hamWordsSet)
            #
            # self.uniqueSpamWords['spam']= self.spamWordsSet.difference(self.commonWords)
            # self.uniqueHamWords['ham']=self.hamWordsSet.difference(self.commonWords)
            #
            # self.mailList[self.mailCnt] = [(lineList[c],lineList[c+1]) for c in range(0,length-1,2)]
            # self.mailWordFreq[self.mailCnt] = sum([int(lineList[i]) for i in range(3, length, 2)])