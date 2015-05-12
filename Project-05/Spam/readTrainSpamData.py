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
        self.commonWords = {}
        self.wordSets = list()
        self.spamDict = {}
        self.hamDict = {}
        self.fileContents = {}

    def generateListsFromInputFile(self):
        """
        This function will read the input from the file and store them in data structures
        :return: None
        """
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
        """
        This function will create data structures which will store the Words on Spam/Ham mails
        :return: None
        """

        for key in self.fileContents.keys(): #Entire file is stored in file contents dictionary

            line = self.fileContents[key]
            line = line.strip(' ')
            line = line.strip('\n')

            self.mailCnt += 1
            lineList = line.split(' ')
            length = len(lineList)


            if lineList[1] == 'spam':   #Each word in the spam mail is taken and the count of it is stored against the word in a dictioanry
                self.spamCnt += 1 #count of spam mails
                for idx in range(2,length-1, 2):
                    val = lineList[idx]
                    if val in self.spamDict.keys():
                        self.spamDict[val] += 1
                    else:
                        self.spamDict[val] = 1

            else: #Each word in ham mail is taken and count of it stored against the word in a dictionary
                self.hamCnt += 1 #count of ham mails
                for idx in range(2,length-1,2):
                    val = lineList[idx]
                    # wordsSet.add(val)
                    if val in self.hamDict.keys():
                    #print "Spam:", val,lineList[idx+1]
                        self.hamDict[val] += 1
                    else:

                        self.hamDict[val] = 1

        #The words which are there commonly in ham and spam mails
        for key in self.spamDict.keys():
            if key in self.hamDict.keys():
                self.commonWords[key] = self.spamDict[key] + self.hamDict[key]



