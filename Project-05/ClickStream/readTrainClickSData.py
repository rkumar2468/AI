__author__ = 'sri'

import os,sys

class readInputData:

    def __init__(self,trainfeat, trainlabs, featnames):
        self.fileTrainFeat = trainfeat
        self.fileTrainLabels = trainlabs
        self.fileFeatNames = featnames
        self.exCnt = 0
        self.featCnt = 0
        self.trainFeatDict = {}
        self.trainLabels= {} #Dictionary with the user ID as key and the class(WillVisit=1/WillVisit=0) as value
        self.featureNames = list()
        self.featureList = {} #Dictionary with feature name as key and its corresponding domain as value
        self.featureDiv = {} #Dictionary which will divide the domain of feature values into 4 sets

    def generateFileDS(self):
        if not os.path.exists(self.fileTrainFeat):
            print "trainfeat file does not exists"
            sys.exit(-1)

        fileTrainFeat = open(self.fileTrainFeat,'r')

        if not os.path.exists(self.fileTrainLabels):
            print "trainlabels file does not exists"
            sys.exit(-1)

        fileTrainLabs = open(self.fileTrainLabels,'r')

        if not os.path.exists(self.fileFeatNames):
            print "trainlabels file does not exists"
            sys.exit(-1)

        fileFeatNames = open(self.fileFeatNames,'r')

        count = 0
        for line in fileTrainFeat:
            line = line.strip(' ')
            line = line.strip('\n')
            line = line.split(' ')
            self.trainFeatDict[count] = line
            count += 1

        self.exCnt = count
        self.featCnt = len(self.trainFeatDict[0])
        print self.featCnt
        count = 0

        for line in fileTrainLabs:
            line = line.strip(' ')
            line = line.strip('\n')
            self.trainLabels[count] = line
            count += 1

        for line in fileFeatNames:
            line = line.strip(' ')
            line = line.strip('\n')

            self.featureNames.append(line)

        # print "The file contents:\n"
        # print self.trainFeatDict


    def generateInputDS(self):

        featureMatrix = [[0 for x in range (274)] for y in range(40000)]

        for indX in range(40000):
            list= self.trainFeatDict[indX]
            for indJ in range(274):
                featureMatrix[indX][indJ] = list[indJ]


        # for indX in range(40000):
        #     print featureMatrix[indX]

        for indX in range(274):
            feature = self.featureNames[indX]
            domSet = set()
            for indJ in range(40000):
                domSet.add(featureMatrix[indJ][indX])
            self.featureList[feature] = domSet


        # print self.featureList

        for feature in self.featureList.keys():
            domSet = self.featureList[feature]

            retDivList = self.computeMediansList(domSet)
            self.featureDiv[feature] = retDivList

        # print self.featureDiv

    def computeMediansList(self, domains):


        domList = list(domains)
        domList.sort(key=int)
        length = len(domList)

        #print "Before sort:", domains
        #print "After sort:", domList

        med1Idx = (0 + (length -1))/2
        med2Idx = (0 + (med1Idx-1))/2
        med3Idx = ((med1Idx+1) + (length-1))/2

        return [domList[med2Idx], domList[med1Idx], domList[med3Idx]]





