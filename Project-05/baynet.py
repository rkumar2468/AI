import sys, os

class NBayes:
    def __init__(self, testInpFile):
        self.file = testInpFile
        self.fileDict = {}
        self.features = {}
        self.length = 0
        self.classes = {}

    def readTestConfiguration(self):
        if not os.path.exists(self.file):
            print "Error: The file "+self.file+" does not exists.\n"
            sys.exit(-1)
        fid = open(self.file,'r')
        lcnt = 0
        for line in fid:
            if line:
                line = line.strip(' ')
                line = line.strip('\n')
                list = line.split(' ')
                self.fileDict[lcnt] = list
                self.classes[lcnt] = list[1]
                lcnt += 1
        self.length = lcnt
        fid.close()

    def generateDict(self):
        if not self.fileDict:
            print 'No test data found.'
            sys.exit(-1)
        for key in self.fileDict.keys():
            length = len(self.fileDict[key])
            self.features[key] = [self.fileDict[key][i] for i in range(2, length-1, 2)]

    def printFeatures(self):
        for key in self.features.keys():
            print key, ' ==> ', self.features[key]

    def probabilityComputation(self, obj, list):
        pSpam = obj.spamProb
        pHam = obj.hamProb
        spamDict = obj.inp.spamDict
        hamDict = obj.inp.hamDict
        spamCnt = obj.inp.spamCnt
        hamCnt = obj.inp.hamCnt

        pfeaturesSpam = []
        pfeaturesHam = []
        for feature in list:
            if feature in spamDict.keys():
                pfeaturesSpam.append(float(spamDict[feature])/float(spamCnt))
            else:
                pfeaturesSpam.append(float(1)/float(spamCnt))

            if feature in hamDict.keys():
                pfeaturesHam.append(float(hamDict[feature])/float(hamCnt))
            else:
                pfeaturesHam.append(float(1)/float(hamCnt))
        s = reduce(lambda x, y: float(x*y), pfeaturesSpam)
        h = reduce(lambda x, y: float(x*y), pfeaturesHam)
        if float(s*pSpam) > float(h*pHam):
            return 'spam'
        else:
            return 'ham'
        
        # print "Spam Prob : ", float(s*pSpam)
        # print "Ham Prob : ", float(h*pHam)

    def run(self, obj):
        result = {}
        self.readTestConfiguration()
        self.generateDict()
        for key in self.features.keys():
            list = self.features[key]
            result[key] = self.probabilityComputation(obj,list)
        return result