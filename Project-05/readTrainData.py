__author__ = 'sri'

import os,sys

class readInputFile:

    def __init__(self,filename):
        self.file=filename
        self.count=0
        self.mailList={}
        self.mailWordFreq={}
        self.spam=0
        self.ham=0

    def generateListsFromInputFile(self):
        if not os.path.exists(self.file):
            print "Error: The file "+self.file+" does not exists.\n"
            sys.exit(-1)
        f=open(self.file,'r')


        for line in f:
            line=line.strip(' ')
            line=line.strip('\n')

            if line.startswith('/'):
                self.count+=1
                lineList=line.split(' ')

                if lineList[1]=='spam':
                    self.spam+=1
                else:
                    self.ham+=1

                msgList=list()

                for i in range(0,len(lineList)-1,2):
                    tup=(lineList[i],lineList[i+1])
                    msgList.append(tup)

                self.mailList.update({self.count:msgList})

                wordCount=0

                for i in range(3,len(lineList),2):
                    wordCount+=int(lineList[i])

                self.mailWordFreq.update({self.count:wordCount})





