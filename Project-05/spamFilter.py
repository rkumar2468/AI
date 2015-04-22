__author__ = 'sri'

import readTrainData

class spamFilter:

    def __init__(self,filename):
        self.file=filename
        self.spamProb=0
        self.hamProb=0

    def getTrainDetails(self):
        inp= readTrainData.readInputFile(self.file)
        inp.generateListsFromInputFile()
        print "Number of mails in training data:",inp.count
        #print "MailList:\n",inp.mailList
        #print "Word Frequency:\n",inp.mailWordFreq
        print "\nNumber of spam mails:",inp.spam
        print "\nNumber of ham mails:",inp.ham

        self.hamProb=float(inp.ham)/float(inp.count)
        self.spamProb=float(inp.spam)/float(inp.count)

        print "Spam Probability:",self.spamProb
        print "Ham Probability:",self.hamProb


if __name__=='__main__':

    spamObj=spamFilter('spam/data/train')
    spamObj.getTrainDetails()


