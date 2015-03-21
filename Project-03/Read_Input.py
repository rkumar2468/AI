import os, sys

class readInputFile:

    def __init__(self,filename):
        self.file=filename
        self.courseTime={}
        self.courseRecite={}
        self.courseDet={}
        self.courseReq={}
        self.taResp={}
        self.taSkills={}

    def generateListsFromInputFile(self):
        if not os.path.exists(self.file):
            print "Error: File \'%s\' doesnot exists.!" %(self.file)
            sys.exit(-1)
        f=open(self.file,'r')
        count=0
        for l in f:
            line = l.lstrip(' ');
            if ('1.' in line) or ('2.' in line) or ('3.' in line) or ('4.' in line) or ('5.' in line) or ('6.' in line):
                count=count-1
                continue
            if line=='\n' or line=='\r':
                count=count+1
                continue
            str=line.strip('\n')
            stringArr=str.split(',')
            values=[x.lstrip(' ') for x in stringArr[1:]]
            list=self.getFunction(count)
            list.update({stringArr[0]:values})

    def getFunction(self,c):
        if(c==0):
            return self.getCourseTime()
        elif(c==1):
            return self.getCourseRecitations()
        elif(c==2):
            return self.getCourseDetails()
        elif(c==3):
            return self.getCourseRequirements()
        elif(c==4):
            return  self.getTAResponsibilities()
        elif(c==5):
            return self.getTASkills()

    def getCourseTime(self):
        return self.courseTime

    def getCourseRecitations(self):
        return self.courseRecite

    def getCourseDetails(self):
        return self.courseDet

    def getCourseRequirements(self):
        return self.courseReq

    def getTAResponsibilities(self):
        return self.taResp

    def getTASkills(self):
        return self.taSkills

    def printCourseTime(self):
        print self.courseTime
