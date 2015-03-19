import re, copy, sys
import Read_Input

class CSP:

    def __init__(self):
        self.assignment = {}
        self.variables = {}
        self.courseTACount = {}
        self.assignee = {}
        self.inp = None
        # Default Values #
        self.recitationTime = 90
        self.classTime = 90

    def reset(self):
        self.assignment = {}
        self.variables = {}
        self.assignee = {}
        self.courseTACount = {}

    def isCourseAssignmentComplete(self, assignment):
        return ([0]*len(assignment) == assignment)

    def isAssignmentComplete(self):

        # To check if the all the courses have a TA assigned #
        if self.isCourseAssignmentComplete(self.assignee.values()):
            return True

        varLen = len(self.variables.keys())
        assignLen = len(self.assignment.keys())
        if varLen == 0 or assignLen == 0:
            return False
        ## Pending: Need to call a function which checks if all the TAs are 100% assigned ##

        return (varLen == assignLen)

    def timeToNum(self, str):
        """
        This function converts the time in the format HH:MI AM/PM to an integer(into minutes)
        :param : str- Time
        :return: integer value of the Time
        """
        ret = 0
        list = str.split(':')
        ampm = list.pop(-1).split(' ')
        list.append(ampm[0])
        if list[0] != '12' and ampm[-1] == 'PM':
            ret =  12*60
        ret += (int(list[0])*60 + int(list[1]))
        return ret

    def timeRangeCheck(self, classReciteTime, taClassTime, classTime, reciteTime):
        """
        This function checks if there is any overlap between the course timings and the TA non-availability timings.
        Returns True if there is no overlap else returns False.
        :param : taTime
        :param : reciteTime
        :param : timePeriod in minutes
        :return: True/False
        """
        if classReciteTime == taClassTime: return False
        if taClassTime > classReciteTime and  taClassTime <= classReciteTime + reciteTime:
            return False
        elif classReciteTime > taClassTime and  classReciteTime <= taClassTime + classTime:
            return False
        return True

    def isTARequiredToAttendClass(self, course):
        """
        This function estimates if a course requires a TA to attend it.
        :param : Course
        :param: inp - object of Read_Input.readInputFile
        :return: True/False
        """
        cDet = self.inp.getCourseDetails()
        if cDet[course][1].lower().strip(' ') == "yes":
            return True
        else:
            return False

    def recitationConstraintCheck(self, ta, course):
        """
        This function checks if the TA is free during the course recitation time
        :param : TA
        :param : Course
        :param : inp: object of Read_Input.readInputFile
        :param : TimePeriod - Duration of recitation
        :return: True/ False
        """
        recitationList = self.inp.getCourseRecitations()

        # If Class doesnt have any Recitations then no point in checking for further constraints. #
        if course not in recitationList.keys():
            return True
        recitations = recitationList[course]
        responsibilities = self.inp.getTAResponsibilities()[ta]
        if recitations[0] != responsibilities[0]:
            return True
        classReciteTime = self.timeToNum(recitations[1])
        taClassTime = self.timeToNum(responsibilities[1])
        # print "Recitation check for [", ta, course, "]"
        return self.timeRangeCheck(classReciteTime, taClassTime, self.classTime, self.recitationTime)

    def skillTest(self, ta, course):
        """
        This function identifies whether the TA possesses all the skills required by the course
        :param : TA name
        :param : Course
        :param : inp - object of Read_Input.readInputFile
        :return: True/False
        """
        taSkill = self.inp.getTASkills()
        courseReq = self.inp.getCourseRequirements()

        # Assumption : If TA doesnt have any skill, just returning False. #
        # Not sure if this is really needed ?? #

        if ta not in taSkill.keys() or len(taSkill[ta]) == 0: return False
        if course not in courseReq.keys(): return True

        # Assumption : If the course doesnt have any requirements, then any TA can be allotted. #
        lenCourse = len(courseReq[course])
        # if lenCourse == 0: return True
        # print taSkill[ta]
        list = [x for x in courseReq[course] if x not in taSkill[ta]]
        # print courseReq[course]
        percent = float(len(list))/float(lenCourse)
        if len(list) != 0 and percent > 0.8:
            # print "Skill Test failed for ta: %s Course: %s" %(ta, course)
            return False
        # print "\nSkill matches for ta: %s Course: %s\n" %(ta, course)
        return True

    def computeTACntForClass(self):
        """
        This function computes the number of TAs required for each course.
        :param : inp - object of Read_Input.readInputFile
        :return : void
        """
        cDet = self.inp.getCourseDetails()
        for key in cDet.keys():
            stud = int(cDet[key][0].strip(' '))
            if stud >= 25 and stud < 40:
                self.courseTACount[key] = 0.5
            elif stud >= 40 and stud < 60:
                self.courseTACount[key] = 1.5
            elif stud >= 60:
                self.courseTACount[key] = 2
            else :
                self.courseTACount[key] = 0
        # print self.courseTACount

    def updateValues(self, filename, recitationTime=90, classTime=90):
        """
        This function generates all the data structures by parsing the input file.
        :return: readInputFile object
        """
        inp = Read_Input.readInputFile(filename)
        inp.generateListsFromInputFile()
        self.inp = inp
        self.recitationTime = recitationTime
        self.classTime = classTime
        self.computeTACntForClass()
        tas = inp.getTAResponsibilities().keys()
        for ta in tas:
            self.variables[ta] = 1
        for course in inp.getCourseTime().keys():
            self.assignee[course] = self.courseTACount[course]
        # return inp

    def addToAssignment(self, ta, assignment):
        # print "Adding assignment [", ta, assignment, "]"
        if self.variables[ta] == 0:
            return 0
        if self.assignee[assignment] <= 1:
            if ta in self.assignment.keys():
                # Need to change it for proper formatting - Done #
                # There are potential issues with this assignment #
                # self.assignee should be updated or else will have issues - Not required#
                self.assignment[ta].append([assignment, self.assignee[assignment]])
            else:
                self.assignment[ta] = [[assignment, self.assignee[assignment]]]
            self.variables[ta] -= self.assignee[assignment]
            # Need to change - Not here but in the next control block(else) #
            return self.assignee[assignment]
        else:
            taOccupancy = 1 - self.variables[ta]
            if ta in self.assignment.keys():
                self.assignment[ta].append([assignment, taOccupancy])
            else:
                self.assignment[ta] = [[assignment, taOccupancy]]
            self.variables[ta] -= taOccupancy
            # Need to change - Changed from 1 to taOccupancy#
            return taOccupancy

    def removeFromAssignment(self, ta, assignment):
        # print "Removing assignment [", ta, assignment, "]"
        # Same issues persists as of add function #]]]
        if self.assignee[assignment] <= 1:
            list = self.assignment[ta]
            list.pop()
            if len(list) != 0:
                self.assignment[ta] = list
            else:
                self.assignment.pop(ta)
            self.variables[ta] += self.assignee[assignment]
        else:
            self.assignment.pop(ta)
            self.variables[ta] += 1

    def backtracking_search(self, var, assign):
        # Assumption is if all TAs are assigned for their Full Time availability #
        # Then it is considered as assignment complete or if all the courses have their assignment complete #
        result = False
        if self.isAssignmentComplete() == True:
            return True
        tas = copy.deepcopy(var)
        values = copy.deepcopy(assign)
        while len(tas) != 0:
            ta = tas.popitem()
            for val in values.keys():
                if self.variables[ta[0]] == 0:
                    return True
                # Added extra condition to eliminate already completed assignments #
                if self.constraintCheck(ta[0], val) and values[val] != 0:
                    # values.pop(val)
                    change = self.addToAssignment(ta[0], val)
                    values[val] -= change
                    if self.variables[ta[0]] == 0:
                        result = self.backtracking_search(tas, values)
                    if result == True:
                        # print "Assignment Succeeded.!"
                        return True
                    # Problem is here #
                    elif self.variables[ta[0]] == 0:
                        self.removeFromAssignment(ta[0], val)
                        values[val] += change
        # temp = values
        if self.isCourseAssignmentComplete(values.values()):
            return True
        return False


    def checkIfTAIsFree(self, ta, course):
        # self.inp.printCourseTime()
        courseTimings = self.inp.getCourseTime()[course]

        # Need to revisit #
        if len(courseTimings)%2 != 0:
            print "Course Timings Error for the course: ", course
            sys.exit(-1)

        responsibilities = self.inp.getTAResponsibilities()[ta]
        # print courseTimings, responsibilities
        if courseTimings[0] != responsibilities[0] and courseTimings[2] != responsibilities[0]:
            return True

        taClassTime = self.timeToNum(responsibilities[1])

        if courseTimings[0] == responsibilities[0]:
            courseFirstTime = self.timeToNum(courseTimings[1])
            # print taClassTime, courseFirstTime
            if not self.timeRangeCheck(courseFirstTime,taClassTime,self.classTime,self.classTime):
                return False
        if courseTimings[2] == responsibilities[0]:
            courseFirstTime = self.timeToNum(courseTimings[3])
            # print taClassTime, courseFirstTime
            if not self.timeRangeCheck(courseFirstTime,taClassTime,self.classTime,self.classTime):
                return False

        # print courseTimings
        return True

    def constraintCheck(self, ta, course):

        # Check if the course is already filled/TA Not required #
            # This check can be done in backtracking search #
        # Check if TA has all the required skills #
        if not self.skillTest(ta, course): return False

        # Check if TA Class timings doesnt class with Course Recitations #
        if not self.recitationConstraintCheck(ta, course): return False

        # Check if TA has to attend the class, if yes TA has to be free during the class timings #
        if self.isTARequiredToAttendClass(course):
            return self.checkIfTAIsFree(ta, course)

        # If the control comes here, all the Cases are passed #
        return True

if __name__ == '__main__':
    print ("Testing CSP.!")
    obj = CSP()
    obj.updateValues('dataset_AI_CSP')
    # obj.updateValues('testInput')
    ret = obj.backtracking_search(obj.variables, obj.assignee)
    if ret == False:
        print "Complete Assignment failed. Only partial assignment done.!\n"
    print "Variables : ", obj.variables
    print
    print "Assignees: ", obj.assignee, "\n"
    # print obj.assignment
    f=open('test.txt','w')
    for keys in obj.assignment.keys():
        print >> f, "Key - ", keys, " Val: ", obj.assignment[keys], "\n"
    f.close()
    # print obj.courseTACount
