__author__ = 'sri'

import readTrainSpamData, baynet
import os, sys
import timeit

class spamFilter:

    def __init__(self,filename):
        self.file=filename
        self.spamProb=0
        self.hamProb=0
        self.inp = None

    def getTrainDetails(self):
        """
        This function creates on object of the readInputFile class and calculates the prior Spam and Ham probabilities
        :return: None
        """
        self.inp = readTrainSpamData.readInputFile(self.file)
        self.inp.generateListsFromInputFile()

        self.hamProb=float(self.inp.hamCnt)/float(self.inp.mailCnt) #Probability of a mail being Spam
        self.spamProb=float(self.inp.spamCnt)/float(self.inp.mailCnt) #Probability of a mail being Ham

if __name__=='__main__':
    startTime=timeit.default_timer() # The time when the program starts execution
    spamObj = spamFilter('spam_data/train') #spamFilter class object - train data file
    spamObj.getTrainDetails()
    nb = baynet.NBayes('spam_data/test') #Test input file is provided

    print "Enter choice:\n1. All words as features\n2. Words in more than 500 mails as features:\n3.Words in more than 500 but less than" \
          " 700 mails as features:"
    choice = input()

    if choice == '' or not (choice == 1 or choice == 2 or choice == 3):
         print "Wrong choice!"
         sys.exit(-1)

    result = nb.run(spamObj, choice) #The run function of NBayes class returns a list of predictions for all the mails in the test data

    endTime=timeit.default_timer() # The time when the backtracking search ends its execution
    runTime=endTime-startTime #Total time taken for the algorithm to execute

    falseCnt = 0
    for key in result.keys():
        if result[key] != nb.classes[key]:
            falseCnt += 1 #total number of false predictions

    print "Accuracy of Prediction: ", (1 - (float(falseCnt)/float(nb.length)))*float(100), "%" #Accuracy
    print "Total Time taken:", runTime