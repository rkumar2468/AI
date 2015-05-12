import sys,os

class NBayes:
    def __init__(self, testInpFile):
        self.file = testInpFile # input Test file
        self.fileDict = {} # Dictionary that contains the entire file
        self.features = {} # Dictionary of all the words of a mail as features
        self.commonFeatures = list() # Dictionary of the common words of spam and ham as features
        self.length = 0 # Number of lines in the file
        self.classes = {} # Dictionary which maintains the class of each mail: Spam or Ham

    def readTestConfiguration(self):
        """
        This function reads the entire input file and creates a Dictionary will keys as mail IDs and value as the
        corresponding mail contents.
        :return: None
        """
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
        self.length = lcnt #Total number of lines in the file
        fid.close()

    def generateFeatures(self, obj, choice):
        """
        This function generates features depending on the choice of the user. If choice is 1 then all the words in the mail are
        considered as features. If choice is 2, common words of Spam and Ham mails from training data are considered as features.
        :param obj: Training data object
        :param choice: Input choice
        :return: None
        """
        if not self.fileDict:
            print 'No test data found.'
            sys.exit(-1)

        for key in self.fileDict.keys():
            length = len(self.fileDict[key])
            self.features[key] = [self.fileDict[key][i] for i in range(2, length-1, 2)]

        if choice == 2:
            for key in obj.inp.commonWords.keys():
                     if obj.inp.commonWords[key] > 500: #Only those common words which are in more than 500 mails are considered
                        self.commonFeatures.append(key)
        elif choice == 3:
            for key in obj.inp.commonWords.keys():
                     if obj.inp.commonWords[key] >= 500 and obj.inp.commonWords[key] <= 700:
                        self.commonFeatures.append(key)


    def printFeatures(self):
        """
        This function prints the features.
        :return: None
        """
        for key in self.features.keys():
            print key, ' ==> ', self.features[key]

    def probabilityComputation(self, obj, list):
        """
        This function will classify a mail as spam or ham based on computation of conditional probabilities.
        :param obj: Training data object
        :param list: Feature list
        :return: spam/ham
        """
        pSpam = obj.spamProb
        pHam = obj.hamProb
        spamDict = obj.inp.spamDict
        hamDict = obj.inp.hamDict
        spamCnt = obj.inp.spamCnt
        hamCnt = obj.inp.hamCnt
        mailCnt = obj.inp.mailCnt

        pfeaturesSpam = []
        pfeaturesHam = []

        for feature in list:
            if feature in spamDict.keys(): # estimating the probability of the feature being present in spam mail
                pfeaturesSpam.append(float(spamDict[feature])/float(spamCnt))
            else:
                #Laplace smoothing
                pfeaturesSpam.append(float(1)/float(mailCnt))

            if feature in hamDict.keys(): # estimating the probability of the feature being present in spam mail
                pfeaturesHam.append(float(hamDict[feature])/float(hamCnt))
            else:
                pfeaturesHam.append(float(1)/float(mailCnt))

        s = reduce(lambda x, y: float(x*y), pfeaturesSpam) # Product of all posterior probabilities
        h = reduce(lambda x, y: float(x*y), pfeaturesHam)

        #If the posterior probability that the mail is spam is greater than the posterior probability
        #the mail is ham; then the mail is classified as spam otherwise as ham.
        if float(s*pSpam) > float(h*pHam):
            return 'spam'
        else:
            return 'ham'

    def run(self, obj, choice):
        """
        This function will be called from the spamFilter.py file which will return the list of classification of all the
        mails in the test input as spam or ham
        :param obj: Training data object
        :param choice: Input choice for what features to be considered
        :return: a list of classifications
        """
        result = {}
        self.readTestConfiguration()
        self.generateFeatures(obj, choice)

        if choice == 1: #The entire mail words are considered as features
             for key in self.features.keys():
                l = self.features[key]
                result[key] = self.probabilityComputation(obj, l)

        else: #Common words are considered as features
            for mail in self.features.keys():
                wordsList = list()
                l = self.features[mail]

                for word in l:
                    if word in self.commonFeatures:
                        wordsList.append(word)

                if len(wordsList) != 0:
                    result[mail] = self.probabilityComputation(obj,wordsList)

        return result #List of predictions