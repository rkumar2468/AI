__author__ = 'sri'

import readTrainData
import os, sys

class spamFilter:

    def __init__(self,filename):
        self.file=filename
        self.spamProb=0
        self.hamProb=0

    def getTrainDetails(self):
        sys.stdout = open("output.txt",'w')
        inp= readTrainData.readInputFile(self.file)
        inp.generateListsFromInputFile()
        # print "Number of mails in training data:",inp.mailCnt
        #print "MailList:\n",inp.mailList
        #print "Word Frequency:\n",inp.mailWordFreq
        # print "\nNumber of spam mails:",inp.spamCnt
        # print "\nNumber of ham mails:",inp.hamCnt
        # print "\nWords in spam mails:", inp.spamWordsSet
        # print "\nWords in ham mails", inp.hamWordsSet
        # print "\nWords that are common in spam and ham:", inp.commonWords
        # print "\nUnique spam words:", inp.uniqueSpamWords
        # print "\nUnique ham words:", inp.uniqueHamWords
        print('Spam Dict: \n')
        for key in inp.spamDict.keys():
            if key in inp.commonWords:
                print key, min(inp.spamDict[key]), max(inp.spamDict[key])
        print('Ham Dict: \n')
        for key in inp.hamDict.keys():
            if key in inp.commonWords:
                print key, min(inp.hamDict[key]), max(inp.hamDict[key])

        self.hamProb=float(inp.hamCnt)/float(inp.mailCnt)
        self.spamProb=float(inp.spamCnt)/float(inp.mailCnt)

        # print "Spam Probability:",self.spamProb
        # print "Ham Probability:",self.hamProb



if __name__=='__main__':

    spamObj=spamFilter('spam/data/train')
    spamObj.getTrainDetails()


