class readInputFile:

    def __init__(self,filename):
        self.file=filename
        self.courseTime={}
        self.courseRecite={}
        self.courseDet={}
        self.courseReq={}
        self.taResp={}
        self.taSkills={}


    def generateFromInputFile(self):
        f=open(self.file,'r')
        count=0
        for line in f:
            if ('1.' in line) or ('2.' in line) or ('3.' in line) or ('4.' in line) or ('5.' in line) or ('6.' in line):
                count=count-1
                continue
            if line=='\n' or line=='\r':
                count=count+1
                continue
            str=line.strip('\n')
            stringArr=str.split(',')
            values=stringArr[1:]
            list=self.getFunction(count)
            list.update({stringArr[0]:values})

    def getFunction(self,c):

        if(c==0):
            return self.getCourseTime()
        if(c==1):
            return self.getCourseRecite()
        if(c==2):
            return self.getCourseDet()
        if(c==3):
            return self.getCourseReq()
        if(c==4):
            return  self.getTAResp()
        if(c==5):
            return self.getTASkills()

    def getCourseTime(self):
        return self.courseTime

    def getCourseRecite(self):
        return self.courseRecite

    def getCourseDet(self):
        return self.courseDet

    def getCourseReq(self):
        return self.courseReq

    def getTAResp(self):
        return self.taResp

    def getTASkills(self):
        return self.taSkills

    def printCourseTime(self):
        print self.courseTime

if __name__ =='__main__':

    # filename=raw_input()
    # print "filename:",filename
    filename = 'dataset_AI_CSP'
    f=readInputFile(filename)
    f.generateFromInputFile()

    log=open("logfile.txt","w")

    print "Course timings:"
    print f.getCourseTime()

    print "Course Recitations:"
    print f.getCourseRecite()

    print "Course Requirements:"
    print f.getCourseReq()

    print "Course Details:"
    print f.getCourseDet()

    print "TA Skills:"
    print f.getTASkills()

    print "TA Responsibilities:"
    print f.getTAResp()

    """
    print >> log, "Course timings:"
    print >> log, f.getCourseTime()

    print >> log, "Course Recitations:"
    print >> log, f.getCourseRecite()

    print >> log,"Course Requirements:"
    print >> log,f.getCourseReq()

    print >> log, "Course Details:"
    print >> log, f.getCourseDet()

    print >> log, "TA Skills:"
    print >> log, f.getTASkills()

    print >> log, "TA Responsibilities:"
    print >> log, f.getTAResp()
    """
