__author__ = 'sri'

import os,sys
import math
import readTrainClickSData
import copy
import Tree
import classifyInput
import timeit

headNode = None
class decisionTree:
    """
    This class creates the decision tree for learning.
    """

    def __init__(self, trainfeat, trainlabs, featnames):
        self.trainFeatFile = trainfeat #training examples file
        self.trainLabFile = trainlabs #training labels files
        self.featuresFile = featnames #features file
        self.inp = None #Training data input object
        self.trainExamples = None #The matrix which consists of the training examples and corresponding feature values
        self.trainFeatures = {} #training features dictionary
        self.trainLabels = [] #training labels list
        self.levelFeatDict = {} #Dictionary of features at each level
        self.level = -1 #Level of the decision tree

    def getTrainDetails(self):
        """
        This function creates on object of readInputData class and generates all required data structures
        :return: None
        """
        self.inp = readTrainClickSData.readInputData(self.trainFeatFile, self.trainLabFile, self.featuresFile)
        self.inp.generateFileDS()
        self.inp.generateInputDS()
        self.trainExamples = copy.deepcopy(self.inp.featureMatrix)
        self.trainFeatures = copy.deepcopy(self.inp.featureList)
        self.trainLabels = copy.deepcopy(self.inp.trainLabels)

    def computeRootEntropy(self, examples, labels):
        """
        This function calculates the entropy of the root node
        :param examples: Matrix of training examples
        :param labels: Training labels
        :return: Entropy of the root node
        """

        trueCnt = 0 #Count of examples for which the goal is true
        falseCnt = 0 #Count of examples for which the goal is false
        exCnt = len(examples)

        for i in range(exCnt):
                if labels[i] == '1':
                    trueCnt += 1

                elif labels[i] == '0':
                    falseCnt += 1

        probTrue = float(trueCnt)/float(exCnt) #Probability of the examples having the goal as true
        probFalse = float(falseCnt)/float(exCnt) #Probability of the examples having goal as false

        if probTrue != 0:
            entTrue= probTrue * math.log(probTrue, 2)
        else:
            entTrue = 0

        if probFalse != 0:
            entFalse = probFalse * math.log(probFalse, 2)
        else:
            entFalse = 0

        entropy = -(entTrue + entFalse) #Entropy

        return entropy


    def computeCounts(self, examples, labels,feature):
        """
        This function will calculate the number of positive
        :param examples: Matrix of training examples
        :param labels: Training labels
        :param feature: The given feature(child)
        :return: domValCnt (total count of examples)
                domValCntList (list of counts of examples corresponding to each value of the feature);
                pList (list of counts of examples corresponding to each value of feature which have goal as True);
                nList (list of counts of examples corresponding to each value of feature which have goal as False)
        """

        val = self.inp.featureDiv[feature] #The different values for feature

        # The count of examples corresponding to each feature value
        domVal1Cnt = 0
        domVal2Cnt = 0


        # The count of examples corresponding to each feature value for which the goal is True
        pCnt1 = 0
        pCnt2 = 0


        # The count of examples corresponding to each feature value for which the goal is False
        nCnt1 = 0
        nCnt2 = 0


        domValCnt = len(examples) #Total number of examples

        for i in range(domValCnt):
            if float(examples[i][feature]) <= float(val): #feature value 1
                domVal1Cnt += 1
                if labels[i] == '1':
                    pCnt1 += 1
                elif labels[i] == '0':
                    nCnt1 += 1

            if float(examples[i][feature]) > float(val):
                domVal2Cnt += 1
                if labels[i] == '1':
                    pCnt2 += 1
                elif labels[i] == '0':
                    nCnt2 += 1


        domValCntList = [domVal1Cnt, domVal2Cnt]
        pList = [pCnt1, pCnt2]
        nList = [nCnt1, nCnt2]


        return domValCnt, domValCntList, pList, nList

    def computeInfoGain(self, examples, labels, feature):
        """
        This function computes the information gain with respect to the feature
        :param examples: Matrix of training examples
        :param labels: Training labels
        :param feature: The given feature(child)
        :return: information gain
        """

        rootFeatEntropy = self.computeRootEntropy(examples, labels) #Entropy of the root feature


        domValCnt, domValCntList, pList, nList = self.computeCounts(examples, labels, feature)

        entropyList = [] #List of entropies corresponding to each feature value

        for i in range(2):
            if domValCntList[i] != 0:
                probTrue = float(pList[i])/float(domValCntList[i])
                probFalse = float(nList[i])/float(domValCntList[i])
            else:
                probTrue = 0
                probFalse = 0

            if probTrue != 0:
                entTrue= probTrue * math.log(probTrue, 2)
            else:
                entTrue = 0

            if probFalse != 0:
                entFalse = probFalse * math.log(probFalse, 2)
            else:
                entFalse = 0

            ent = -(entTrue + entFalse)

            entropyList.append(ent)

        childFeatEntropy = 0

        for i in range(2):
            childFeatEntropy += (float(domValCntList[i])/float(domValCnt))*entropyList[i]

        #Information gain with respect to feature
        infoGain = rootFeatEntropy - childFeatEntropy

        return infoGain

    def getBestAttribute(self, examples, labels, features):
        """
        This function computes the feature with maximum information gain
        :param examples: Matrix of training examples
        :param labels: Training labels
        :param feature: The given feature(child)
        :return: feature with maximum info gain
        """
        length = len(examples)

        gainList = {} #Information gain with respect to all features
        for key in features.keys():
            infoGain = self.computeInfoGain(examples, labels, key)
            gainList[key] = infoGain


        #Maximum information gain
        maxInfoGain = max(gainList.values())

        # feature with maximum info gain
        for key in gainList:
            if float(gainList[key]) == (maxInfoGain):
                feature = key
                break



        return feature


    def decisionTree_Learning(self, examples, labels, default, currentNode, level):
        """
        This function will construct the decision tree
        :param examples: Matrix of training examples
        :param labels: Training labels
        :param feature: Dictionary of all features
        :param default: initial default value of the goal
        :return: decision tree
        """

        print "In decision tree learning; Initial level:", level

        global headNode
        setLabs = set(labels) #Label set

        tree = Tree.TreeTraversals(currentNode)

        #If there are no more examples, the default value of the root is returned as classification
        if not examples:
            currNode = Tree.Node(default)
            print "No more examples; Tree Root Val:",currNode.value

        #If the labels are all '1' or all '0' , the classification is returned
        elif len(setLabs) == 1:
            if '1' in setLabs:
                currNode = Tree.Node('Yes')
                print "Classify,Tree Root Val:",currNode.value
            if '0' in setLabs:
                currNode = Tree.Node('No')
                print "Classify,Tree Root Val:",currNode.value

        #If there are no more features left, then majority value of the labels is returned as classification
        elif bool(self.levelFeatDict) == False and currentNode != None:
            currNode = Tree.Node(self.getMajorityValue(labels))
            print "No more features,Tree Root Val:", currNode.value

        else:
            #The feature with maximum info gain
            if currentNode == None:
                root = self.getBestAttribute(examples, labels, self.trainFeatures)
                newFeatures = copy.deepcopy(self.trainFeatures)
                newFeatures.pop(root)
            else:
                if level in self.levelFeatDict.keys():
                    newFeatures = self.levelFeatDict[level]
                    root = self.getBestAttribute(examples,labels,newFeatures)
                    newFeatures.pop(root)
                else:
                    newFeatures = copy.deepcopy(self.trainFeatures)
                    parentList = tree.getParentList()
                    parentList.append(currentNode.getValue())
                    for parent in parentList:
                        newFeatures.pop(parent)
                    # if currentNode != None:
                    if bool(newFeatures) == False:
                        print "No new features"
                        currNode = Tree.Node(self.getMajorityValue(labels))
                        return currNode
                    root = self.getBestAttribute(examples, labels, newFeatures)


            self.levelFeatDict[level] = newFeatures

            currNode = Tree.Node(root)
            currNode.addDist(self.inp.featureDiv[root])
            if currentNode == None and headNode == None:
                headNode = currNode
            else:
                currentNode.addChildren(currNode)
            print "Current Node:", currNode.getValue()


            #Current majority value
            majorityVal = self.getMajorityValue(labels)


            #Looping through the values of root to find features corresponding to each value
            for i in range(2):
                print "Val:", i
                #Subset of examples and labels corresponding to the value of the feature
                subSetExamples, subSetLabels = self.getExamplesSubset(examples, labels, i, root)

                print "Level Before:", level
                child = self.decisionTree_Learning(subSetExamples, subSetLabels, majorityVal, currNode, level+1)
                print "Level After:", level
                print "Child value ; Parent Value:", child.value, currNode.value
                if child.value in self.levelFeatDict[level]:
                    self.levelFeatDict[level].pop(child.value)

                    #tree.createTree(child.root.value)
                if child.value == 'Yes' or child.value == 'No':
                    currNode.addChildren(child)

            self.levelFeatDict.pop(level)


        return currNode

    def getMajorityValue(self, labels):
        """
        This function will return the majority value of the labels
        :param labels: Training labels
        :return: Yes is majority of the labels are '1' / No if majority of the labels are '0'
        """
        pCnt = 0 #Count of 1s
        nCnt = 0 #Count of 0s

        for i in labels:
            if i == '1':
                pCnt += 1
            else:
                nCnt += 1

        if pCnt >= nCnt:
            return 'Yes'
        else:
            return 'No'

    def getExamplesSubset(self, examples, labels, i, root):
        """
        This function will return the subset of examples and labels corresponding to the value of the root
        :param examples: Matrix of training examples
        :param labels: Training labels
        :param i: Value of the root
        :param root: root feature
        :return: subsetExamples(subset of examples); subsetLabels(subset of labels)
        """
        subsetExamples = []
        subsetLabels = []
        val = self.inp.featureDiv[root]
        exNum = len(examples)
        if i == 0:
            for j in range(exNum):
                if float(examples[j][root]) <= float(val):
                    subsetExamples.append(examples[j])
                    subsetLabels.append(labels[j])
        elif i == 1:
            for j in range(exNum):
                if float(examples[j][root]) > float(val):
                    subsetExamples.append(examples[j])
                    subsetLabels.append(labels[j])

        return subsetExamples, subsetLabels


if __name__ == '__main__':
    sys.stdout = open("output.txt",'w')

    startTime=timeit.default_timer() # The time when the program starts execution

    obj = decisionTree('clickstream/clickstream-data/trainfeat.csv','clickstream/clickstream-data/trainlabs.csv','clickstream/clickstream-data/featnames.csv')
    obj.getTrainDetails()
    obj.decisionTree_Learning(obj.trainExamples, obj.trainLabels, 'Yes', None, 0)
    classifyObj = classifyInput.decisionTreeInduction('clickstream/clickstream-data/testfeat.csv','clickstream/clickstream-data/testlabs.csv')
    classifyObj.generateFileDS()
    labels = classifyObj.classifyTestData(headNode)
    trueCount, accuracy = classifyObj.computeAccuracy()

    endTime=timeit.default_timer() # The time when the backtracking search ends its execution
    runTime=endTime-startTime #Total time taken for the algorithm to execute

    print trueCount
    print "Accuracy:", accuracy
    print "Total Time taken:", runTime






