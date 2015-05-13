__author__ = 'sri'

import os,sys

class readInputData:
    """
    This class will data from the input files and creates data structures
    """
    def __init__(self,trainfeat, trainlabs, featnames):
        self.fileTrainFeat = trainfeat
        self.fileTrainLabels = trainlabs
        self.fileFeatNames = featnames
        self.exCnt = 0
        self.featCnt = 0
        self.trainFeatDict = {}
        self.featureMatrix = None
        self.trainLabels= [] #Dictionary with the user ID as key and the class(WillVisit=1/WillVisit=0) as value
        self.featureNames = list()
        self.featureList = {} #Dictionary with feature number as key and its corresponding domain as value
        self.featureDiv = {} #Dictionary which will divide the domain of feature values into 4 sets
        self.featureDist = {}

    def generateFileDS(self):
        """
        This function will read from the input files and creates file data structures
        :return: None
        """
        if not os.path.exists(self.fileTrainFeat):
            print "trainfeat file does not exists"
            sys.exit(-1)

        fileTrainFeat = open(self.fileTrainFeat,'r') #Training examples file

        if not os.path.exists(self.fileTrainLabels):
            print "trainlabels file does not exists"
            sys.exit(-1)

        fileTrainLabs = open(self.fileTrainLabels,'r') #Training labels file

        if not os.path.exists(self.fileFeatNames):
            print "trainlabels file does not exists"
            sys.exit(-1)

        fileFeatNames = open(self.fileFeatNames,'r') #Feature names file

        count = 0
        for line in fileTrainFeat:
            line = line.strip(' ')
            line = line.strip('\n')
            line = line.split(' ')
            self.trainFeatDict[count] = line #Training examples file data structure
            count += 1

        self.exCnt = count
        self.featCnt = len(self.trainFeatDict[0])
        count = 0

        for line in fileTrainLabs:
            line = line.strip(' ')
            line = line.strip('\n')
            self.trainLabels.append(line) #Training labels file data structure
            count += 1

        for line in fileFeatNames:
            line = line.strip(' ')
            line = line.strip('\n')

            self.featureNames.append(line) #Features file data structure


    def generateInputDS(self):
        """
        This function will create all the required data structures
        :return: None
        """

        self.featureMatrix = [[0 for x in range (self.featCnt)] for y in range(self.exCnt)]

        for indX in range(self.exCnt):
            list= self.trainFeatDict[indX]
            for indJ in range(self.featCnt):
                self.featureMatrix[indX][indJ] = list[indJ]

        feature = 0
        for indX in range(self.featCnt):
            domSet = set()
            for indJ in range(self.exCnt):
                domSet.add(self.featureMatrix[indJ][indX])
            self.featureList[feature] = domSet
            feature += 1

        self.preprocess()


        for feature in self.featureList.keys():
            domSet = self.featureList[feature]

            retDiv = self.computeMediansList(domSet) #List of range of feature values
            print retDiv
            self.featureDiv[feature] = retDiv


    def computeMediansList(self, domains):
        """
        This function will compute value ranges for each feature. The ranges are estimated using median values
        :param domains: List of values corresponding to a feature
        :return: Values ranges for the feature
        """

        domList = list(domains)
        domList.sort(key=int)
        length = len(domList)


        if length > 2:
            med1Idx = (0 + (length -1))/2
        else:
            return domList[0]

        return domList[med1Idx]

    def preprocess(self):
        """
        This function does the pre-processing of data
        :return: None
        """

        count = 0
        for key in self.featureList.keys():

            fList = list(self.featureList[key])
            if(len(fList) <= 6): #All the features which have number of values less, i.e less than or equal to 6 are removed from the feature list
                count += 1
                del self.featureList[key]






