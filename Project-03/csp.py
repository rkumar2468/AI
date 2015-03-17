import re
import Read_Input

class CSP:

    def __init__(self):
        self.assignment = []
        self.variables = []
        self.constraints = []
        self.courseTACount = {}

    def reset(self):
        self.assignment = {}
        self.variables = {}
        # self.constraints = []
        self.assignee = []
        self.courseTACount = {}

    def timeToNum(self, str):
        ret = 0
        list = str.split(':')
        ampm = list.pop(-1).split(' ')
        list.append(ampm[0])
        if ampm[-1] == 'PM':
            ret =  12*60
        ret += (int(list[0])*60 + int(list[1]))
        return ret

    def timeRangeCheck(self, taTime, reciteTime):
        """
        This function checks whether there is any overlap in 90 mins of either times.
        Returns True if they doesnt overlap else Returns False.

        :param taTime:
        :param reciteTime:
        :return: True/False
        """
        if taTime == reciteTime: return False
        if reciteTime > taTime and  reciteTime <= taTime + 90:
            return False
        elif taTime > reciteTime and  taTime <= reciteTime + 90:
            return False
        return True

    def recitationConstraintCheck(self, ta, course, inp):
        recitations = inp.getCourseRecitations()[course]
        responsibilities = inp.getTAResponsibilities()[ta]
        if recitations[0] != responsibilities[0]:
            return True
        taTime = self.timeToNum(recitations[1])
        reciteTime = self.timeToNum(responsibilities[1])
        return self.timeRangeCheck(taTime, reciteTime)


    def skillTest(self, ta, course, inp):
        """
        This function identifies whether the TA matches all the course requirements.
        :param ta:
        :param course:
        :param inp:
        :return: True/False
        """
        taSkill = inp.getTASkills()
        courseReq = inp.getCourseRequirements()
        list = [x for x in taSkill[ta] if x not in courseReq[course]]
        # print courseReq[course]
        if len(list) != 0:
            return False
        return True

    def isTARequired(self, course, inp):
        """
        Does the TA needs to attend the class
        :return: True/False
        """
        cDet = inp.getCourseDetails()
        if cDet[course][1] == 'yes':
            return True
        else:
            return False

    def computeTACntForClass(self, inp):
        """
        This function is responsible for computing how many TAs needed for each course.
        :param inp: Read_Input.readInputFile
        :return: void
        """
        cDet = inp.getCourseDetails()
        for key in cDet.keys():
            stud = cDet[key][0].strip(' ')
            if stud >= 25 and stud < 40:
                self.courseTACount[key] = 0.5
            elif stud >= 40 and stud < 60:
                self.courseTACount[key] = 1.5
            elif stud >= 60:
                self.courseTACount[key] = 2
        # print self.courseTACount

    def updateValues(self, filename):
        """
        Generates all the basic data structures based on the input file.
        :return: readInputFile object
        """
        inp = Read_Input.readInputFile(filename)
        inp.generateListsFromInputFile()
        # self.variables = inp.getTAResp().keys()
        return inp

    def bactracking_search(self):
        print "help"

    # def constraintCheck(self):

if __name__ == '__main__':
    print ("Testing CSP.!")
    obj = CSP()
    # inp = obj.updateValues('dataset_AI_CSP')
    # obj.computeTACntForClass(inp)
    # print "Does TA1 has all the skills for RAJ? ", obj.skillTest('TA1','RAJ',inp)
    print obj.timeRangeCheck(obj.timeToNum('2:30 PM'), obj.timeToNum('2:30 AM'))
    print
    # print " TAs Count: ", len(obj.variables)
    # print
    # print obj.timeToNum('2:30 PM')