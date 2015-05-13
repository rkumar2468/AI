__author__ = 'sri'

import os,sys

class decisionTreeInduction:

    def __init__(self, testFeat, testLabels):
        self.fileTestFeat = testFeat #input file which consists of all examples and corresponding feature values
        self.fileTestLabels = testLabels #input file containing labels
        self.testFeatDict = {} # dictionary of all examples
        self.testLabels = [] # list of labels
        self.exCnt = 0 #Number of examples in the given test data
        self.classifyLabels = []

    def generateFileDS(self):
        """
        The test input files are parsed and corresponding data structures are created
        :return:
        """
        if not os.path.exists(self.fileTestFeat):
            print "trainfeat file does not exists"
            sys.exit(-1)

        fileTestFeat = open(self.fileTestFeat,'r') #Test examples file

        if not os.path.exists(self.fileTestLabels):
            print "trainlabels file does not exists"
            sys.exit(-1)

        fileTestLabels = open(self.fileTestLabels,'r') #Test labels file

        count = 0

        for line in fileTestFeat:
            line = line.strip(' ')
            line = line.strip('\n')
            line = line.split(' ')
            self.testFeatDict[count] = line #Test examples file data structure
            count += 1

        self.exCnt = count

        count = 0

        for line in fileTestLabels:
            line = line.strip(' ')
            line = line.strip('\n')
            self.testLabels.append(line) #Test labels file data structure
            count += 1


    def classifyTestData(self, root):
        """
        This function classifies the test examples based on decision tree built
        :param root: Root of the decision tree
        :return: List of labels computed
        """

        for ex in self.testFeatDict.keys():

            label = self.traverseTree(root, self.testFeatDict[ex])
            self.classifyLabels.append(label)

        return self.classifyLabels

    def traverseTree(self, root, features):
        """
        This function will traverse the tree for each example in test data to identify the label
        :param root: The root of the decision tree
        :param features: List of features for the example
        :return: The label '0' or '1'
        """

        children = root.getChildren() #The children of the root
        dist = root.getDistribution() #The value split on the root feature

        if features[root.value] <= dist: #If the value of the feature lies in the first range of domain of the root
            if children[0].value == 'Yes': #If the child is the leaf containing the classification
                return '1'
            elif children[0].value == 'No':
                return '0'
            else: #Else the first child is passed as the root for the next recursive call
                return self.traverseTree(children[0],features )
        else: ##If the value of the feature lies in the second range of domain of the root
            if children[1].value == 'Yes': #If the child is the leaf containing the classification
                return '1'
            elif children[1].value == 'No':
                return '0'
            else: #Else the second child is passed as the root for the next recursive call
                return self.traverseTree(children[1], features)

    def computeAccuracy(self):
        """
        The accuracy of the predictions is computed
        :return: Accuracy, total number of correct predictions
        """
        trueCount = 0
        for i in range (self.exCnt):
            if(int(self.testLabels[i]) == int(self.classifyLabels[i])):
                trueCount += 1

        accuracy = (float(trueCount)/float(self.exCnt)) * float(100)

        return trueCount,accuracy















