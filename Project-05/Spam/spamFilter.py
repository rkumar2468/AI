__author__ = 'sri'

import readTrainSpamData, baynet
import os, sys

class spamFilter:

    def __init__(self,filename):
        self.file=filename
        self.spamProb=0
        self.hamProb=0
        self.inp = None

    def getTrainDetails(self):

        self.inp = readTrainSpamData.readInputFile(self.file)
        self.inp.generateListsFromInputFile()
        # print "Number of mails in training data:",inp.mailCnt
        # print "MailList:\n",inp.mailList
        # print "Word Frequency:\n",inp.mailWordFreq
        # print "\nNumber of spam mails:",inp.spamCnt
        # print "\nNumber of ham mails:",inp.hamCnt
        # print "\nWords in spam mails:", inp.spamWordsSet
        # print "\nWords in ham mails", inp.hamWordsSet
        # print "\nWords that are common in spam and ham:", inp.commonWords
        # print "\nUnique spam words:", inp.uniqueSpamWords
        # print "\nUnique ham words:", inp.uniqueHamWords
        # print('Spam Dict: \n')
        # for key in inp.spamDict.keys():
        #     if key in inp.commonWords:
        #         print key, min(inp.spamDict[key]), max(inp.spamDict[key])
        # print('Ham Dict: \n')
        # for key in inp.hamDict.keys():
        #     if key in inp.commonWords:
        #         print key, min(inp.hamDict[key]), max(inp.hamDict[key])

        ## self.hamProb --> P(H) ##
        ## self.spamProb --> P(S) ##
        self.hamProb=float(self.inp.hamCnt)/float(self.inp.mailCnt)
        self.spamProb=float(self.inp.spamCnt)/float(self.inp.mailCnt)

if __name__=='__main__':

    spamObj = spamFilter('spam/data/train')
    spamObj.getTrainDetails()
    nb = baynet.NBayes('spam/data/test')

    print "Enter choice:\n1. All features\n2. Intersection features:\n"
    choice = input()

    if choice == '' or not (choice == 1 or choice == 2):
         print "Wrong choice!"
         sys.exit(-1)

    result = nb.run(spamObj, choice)
    falseCnt = 0
    for key in result.keys():
        if result[key] != nb.classes[key]:
            falseCnt += 1
    print "False Prediction Occurrences: %s " %(falseCnt)
    print "Accuracy of Prediction: ", (1 - float(falseCnt)/float(nb.length))*float(100), "%"
