__author__ = 'sri'


import os, sys
import math
import readTrainClickSData

class decisionTree:

    def __init__(self, trainfeat, trainlabs, featnames):

        self.trainFeatFile = trainfeat
        self.trainLabFile = trainlabs
        self.featuresFile = featnames
        self.inp = None
        self.visitsEntropy = 0

    def getTrainDetails(self):

        self.inp = readTrainClickSData.readInputData(self.trainFeatFile, self.trainLabFile, self.featuresFile)
        self.inp.generateFileDS()
        self.inp.generateInputDS()

    def computeEntropy(self):

        visitYesCnt = 0
        visitNoCnt = 0

        for key in self.inp.trainLabels.keys():
            if self.inp.trainLabels[key] == '1':
                visitYesCnt += 1
            else:
                visitNoCnt += 1

        probVisitYes = float(visitYesCnt)/float(self.inp.exCnt)
        probVisitNo = float(visitNoCnt)/float(self.inp.exCnt)

        self.visitsEntropy = -((probVisitYes * math.log(probVisitYes, 2)) +(probVisitNo * math.log(probVisitNo, 2)))


if __name__ == '__main__':
    # sys.stdout = open("output.txt",'w')
    obj = decisionTree('clickstream/clickstream-data/trainfeat.csv','clickstream/clickstream-data/trainlabs.csv','clickstream/clickstream-data/featnames.csv')
    obj.getTrainDetails()
    obj.computeEntropy()
    print obj.visitsEntropy


