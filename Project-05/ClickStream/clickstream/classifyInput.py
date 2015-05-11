__author__ = 'sri'

import os,sys
class readTestInput:


    def __init__(self, testfeat, testlabels):
        self.fileTestFeat = testfeat #input test file
        self.fileTestLabels = testlabels #input test labels file
        self.testFeatDict = {} #input test features
        self.testLabelsDict = [] #input test labels
        self.exCnt = 0 #number of examples in test file

        """    def generateFileDS(self):

        This function will read from the input files and creates file data structures
        :return: None
        """
        if not os.path.exists(self.fileTestFeat):
            print "trainfeat file does not exists"
            sys.exit(-1)

        fileTestFeat = open(self.fileTestFeat,'r') #Training examples file

        if not os.path.exists(self.fileTestLabels):
            print "trainlabels file does not exists"
            sys.exit(-1)

        fileTrainLabs = open(self.fileTestLabels,'r') #Training labels file

        count = 0
        for line in fileTestFeat:
            line = line.strip(' ')
            line = line.strip('\n')
            line = line.split(' ')
            self.testFeatDict[count] = line #Training examples file data structure
            count += 1

        self.exCnt = count
        self.featCnt = len(self.testFeatDict[0])
        # print self.featCnt


        for line in fileTrainLabs:
            line = line.strip(' ')
            line = line.strip('\n')
            self.testLabelsDict.append(line) #Training labels file data structure





