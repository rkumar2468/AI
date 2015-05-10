__author__ = 'sri'


import os,sys
import math
import readTrainClickSData
import copy
import Tree


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

    def getTrainDetails(self):
        """
        This function creates on object of readInputData class and generates all required data structures
        :return: None
        """
        self.inp = readTrainClickSData.readInputData(self.trainFeatFile, self.trainLabFile, self.featuresFile)
        self.inp.generateFileDS()
        self.inp.generateInputDS()
        self.inp.calDistribution()
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
        # if valIdx == -1:
        #     self.computeGoalEntropy()
        #     return self.visitsEntropy

        trueCnt = 0 #Count of examples for which the goal is true
        falseCnt = 0 #Count of examples for which the goal is false
        exCnt = len(examples)

        # print "Lables in Compute Entropy:", labels
        for i in range(exCnt):
                if labels[i] == '1':
                    trueCnt += 1

                elif labels[i] == '0':
                    falseCnt += 1

        probTrue = float(trueCnt)/float(exCnt) #Probability of the examples having the goal as true
        probFalse = float(falseCnt)/float(exCnt) #Probability of the examples having goal as false
        # print "Example Cnt:",float(exCnt),float(probTrue),float(probFalse)

        if probTrue != 0:
            entTrue= probTrue * math.log(probTrue, 2)
        else:
            entTrue = 0

        if probFalse != 0:
            entFalse = probFalse * math.log(probFalse, 2)
        else:
            entFalse = 0

        entropy = -(entTrue + entFalse) #Entropy
        # print "Entropy:",entropy

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
        # if valIdx != -1:
        #     domFeat1List = self.inp.featureDiv[feature1]

        domFeat2List = self.inp.featureDiv[feature] #The different values for feature
        # print "Dom Div:",domFeat2List

        # The count of examples corresponding to each feature value
        domVal1Cnt = 0
        domVal2Cnt = 0
        domVal3Cnt = 0
        domVal4Cnt = 0

        # The count of examples corresponding to each feature value for which the goal is True
        pCnt1 = 0
        pCnt2 = 0
        pCnt3 = 0
        pCnt4 = 0

        # The count of examples corresponding to each feature value for which the goal is False
        nCnt1 = 0
        nCnt2 = 0
        nCnt3 = 0
        nCnt4 = 0

        domValCnt = len(examples) #Total number of examples

        for i in range(domValCnt):
            if float(examples[i][feature]) <= float(domFeat2List[0]): #feature value 1
                domVal1Cnt += 1
                if labels[i] == '1':
                    pCnt1 += 1
                elif labels[i] == '0':
                    nCnt1 += 1

            if float(examples[i][feature]) > float(domFeat2List[0]) and float(examples[i][feature]) <= float(domFeat2List[1]): #feature value 2
                domVal2Cnt += 1
                if labels[i] == '1':
                    pCnt2 += 1
                elif labels[i] == '0':
                    nCnt2 += 1

            if float(examples[i][feature]) > float(domFeat2List[1]) and float(examples[i][feature]) <= float(domFeat2List[2]): #feature value 3
                domVal3Cnt += 1
                if labels[i] == '1':
                    pCnt3 += 1
                elif labels[i] == '0':
                    nCnt3 += 1

            if float(examples[i][feature]) > float(domFeat2List[2]): #feature value 4
                domVal4Cnt += 1
                if labels[i] == '1':
                    pCnt4 += 1
                elif labels[i] == '0':
                    nCnt4 += 1


        domValCntList = [domVal1Cnt, domVal2Cnt, domVal3Cnt, domVal4Cnt]
        pList = [pCnt1, pCnt2, pCnt3, pCnt4]
        nList = [nCnt1, nCnt2, nCnt3, nCnt4]

        return domValCnt, domValCntList, pList, nList

    def computeInfoGain(self, examples, labels, feature):
        """
        This function computes the information gain with respect to the feature
        :param examples: Matrix of training examples
        :param labels: Training labels
        :param feature: The given feature(child)
        :return: information gain
        """
        # print "Feature:", feature

        rootFeatEntropy = self.computeRootEntropy(examples, labels) #Entropy of the root feature

        # print "feat1Entropy:\n",feat1Entropy

        domValCnt, domValCntList, pList, nList = self.computeCounts(examples, labels, feature)
        # print "domValCnt:\n",domValCnt
        # print "domValCntList:\n",domValCntList
        # print "pList:\n",pList
        # print "nList:\n",nList

        entropyList = [] #List of entropies corresponding to each feature value

        for i in range(4):
            if domValCntList[i] != 0:
                probTrue = float(pList[i])/float(domValCntList[i])
                probFalse = float(nList[i])/float(domValCntList[i])
            else:
                probTrue = 0
                probFalse = 0
            # print "Prob true and false:",probTrue,probFalse

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

        for i in range(4):
            childFeatEntropy += (float(domValCntList[i])/float(domValCnt))*entropyList[i]

        # print "RootEnt:",rootFeatEntropy
        # print "ChildEnt:",childFeatEntropy

        #Information gain with respect to feature
        infoGain = rootFeatEntropy - childFeatEntropy

        # print "Gain",infoGain

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

        # print "Length of examples in getBestAttribute:",length

        gainList = {} #Information gain with respect to all features
        for key in features:
            infoGain = self.computeInfoGain(examples, labels, key)
            gainList[key] = infoGain

        # print gainList

        #Maximum information gain
        maxInfoGain = max(gainList.values())

        # feature with maximum info gain
        for key in gainList:
            if float(gainList[key]) == (maxInfoGain):
                feature = key
                break

        # print feature, maxInfoGain

        return feature



    def decisionTree_Learning(self, examples, features, labels, default):
        """
        This function will construct the decision tree
        :param examples: Matrix of training examples
        :param labels: Training labels
        :param feature: Dictionary of all features
        :param default: initial default value of the goal
        :return: decision tree
        """

        tree = Tree.Tree() #decision tree

        setLabs = set(labels) #Label set

        #If there are no more examples, the default value of the root is returned as classification
        if not examples:
            tree.createTree(default)
            print "Tree Root Val:",tree.root.value

        #If the labels are all '1' or all '0' , the classification is returned
        elif len(setLabs) == 1:
            if '1' in setLabs:
                tree.createTree('Yes')
                print "Tree Root Val:",tree.root.value
            if '0' in setLabs:
                tree.createTree('No')
                print "Tree Root Val:",tree.root.value

        #If there are no more features left, then majority value of the labels is returned as classification
        elif bool(features) == False:
            tree.createTree(self.getMajorityValue(labels))
            print "Tree Root Val:",tree.root.value
        else:
            # print "Examples in decision tree learning:", examples
            # print "Features in decision tree learning:",features
            # print "Labels in decision tree learning:",labels

            #The feature with maximum info gain
            root = self.getBestAttribute(examples, labels, features)
            print "Root:", root
            tree.createTree(root)

            #Current majority value
            majorityVal = self.getMajorityValue(labels)

            del features[root]
            print "Feature length after removing root:", len(features.keys())

            #Values of the feature
            lenDiv = len(self.inp.featureDiv[root])
            print "Div:", self.inp.featureDiv[root]

            #Looping through the values of root to find features corresponding to each value
            for i in range(lenDiv+1):
                #Subset of examples and labels corresponding to the value of the feature
                subSetExamples, subSetLabels = self.getExamplesSubset(examples, labels, i, root)
                # print "Subset Examples:",subSetExamples
                # print "Length1:",len(subSetExamples)
                # print "Subset Labels:",subSetLabels
                # print "Length2:",len(subSetLabels)
                # child = self.getBestAttribute(subSetExamples, subSetLabels, features)

                #The feature corresonding to value of the root
                child = self.decisionTree_Learning(subSetExamples, features, subSetLabels, majorityVal)
                tree.createTree(child.root.value)
                print "Child and Root ",child.root.value, root
                print "Features before deleting:",features

                # if child.root.value != 'Yes' and child.root.value != 'No' and bool(features) == True:
                #     del features[child.root.value] #Removing the selected feature from the feature list
                # print "Features after deleting:",features

            #   #add node to the root

        return tree

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
        domDivList = self.inp.featureDiv[root]
        exNum = len(examples)
        if i == 0:
            for j in range(exNum):
                if float(examples[j][root]) <= float(domDivList[0]):
                    subsetExamples.append(examples[j])
                    subsetLabels.append(labels[j])
        elif i == 1:
            for j in range(exNum):
                if float(examples[j][root]) > float(domDivList[0]) and float(examples[j][root]) <= float(domDivList[1]):
                    subsetExamples.append(examples[j])
                    subsetLabels.append(labels[j])
        elif i == 2:
            for j in range(exNum):
                if float(examples[j][root]) > float(domDivList[1]) and float(examples[j][root]) <= float(domDivList[2]):
                    subsetExamples.append(examples[j])
                    subsetLabels.append(labels[j])
        elif i == 3:
            for j in range(exNum):
                if float(examples[j][root]) > float(domDivList[2]):
                    subsetExamples.append(examples[j])
                    subsetLabels.append(labels[j])

        return subsetExamples, subsetLabels


if __name__ == '__main__':
    sys.stdout = open("output.txt",'w')
    obj = decisionTree('clickstream/clickstream-data/trainfeat.csv','clickstream/clickstream-data/trainlabs.csv','clickstream/clickstream-data/featnames.csv')
    obj.getTrainDetails()
    #obj.decisionTree_Learning(obj.trainExamples, obj.trainFeatures, obj.trainLabels, 'Yes')



