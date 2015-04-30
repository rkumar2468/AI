__author__ = 'sri'


class decisionTree:

    def __init__(self, trainfeat, trainlabs, featnames):

        self.trainFeatFile = trainfeat
        self.trainLabFile = trainlabs
        self.featuresFile = featnames
        self.inp = None

    def getTrainDetails(self):

        self.inp = readTrainClickSData.readInputData(self.trainFeatFile, self.trainLabFile, self.featuresFile)
        self.inp.generateFileDS()
        self.inp.generateInputDS()