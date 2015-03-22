"""
***Constraint Propagation***
Authors: Rajendra Kumar R; Sri Sruti Mandadapu
"""

import copy, sys
import Read_Input
import timeit

numBSNodes=0
numFCNodes=0
numACNodes=0

class CSP:

    def __init__(self):

        """
        This function is a constructor of the class and initializes all the data structures
        :return:
        """
        self.assignment = {}
        self.variables = {}
        self.courseTACount = {}
        self.assignee = {}
        self.inp = None
        self.recitationTime = 90
        self.classTime = 90
        self.inValidAssign=[]

    def reset(self):
        self.assignment = {}
        self.variables = {}
        self.assignee = {}
        self.courseTACount = {}

    def isCourseAssignmentComplete(self, assignment):
        """
        This function checks if all the courses are assigned with TAs
        :param assignment: Domain values(courses)
        :return: True/False
        """
        return ([0]*len(assignment) == assignment)

    def isAssignmentComplete(self):
        """
        This function checks if the assignment is complete #
        :return: True/False
        """

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

        # The day of the class recitation and the TA's course are different
        if recitations[0] != responsibilities[0]:
            return True

        classReciteTime = self.timeToNum(recitations[1])
        taClassTime = self.timeToNum(responsibilities[1])

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

        # Assumption : If TA doesnt have any skill returning False./ If the course does not have any specific requirement return True #

        #If the TA does not have any skill, return False
        if ta not in taSkill.keys() or len(taSkill[ta]) == 0: return False

        #If the course has no specific skill, return True
        if course not in courseReq.keys(): return True

        lenCourse = len(courseReq[course])

        list = [x for x in courseReq[course] if x not in taSkill[ta]]

        # To check if the TA skills match maximum number of skills the course requires.
        percent = float(len(list))/float(lenCourse)
        if len(list) != 0 and percent > 0.8:
            return False
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


    def updateValues(self, filename, recitationTime=90, classTime=90):
        """
        This function generates all the data structures by parsing the input file.
        :return: void
        """
        inp = Read_Input.readInputFile(filename)
        inp.generateListsFromInputFile()
        self.inp = inp
        self.recitationTime = recitationTime
        self.classTime = classTime
        self.computeTACntForClass()
        tas = inp.getTAResponsibilities().keys()

        # Initializing all the variables(TAs) to 1
        for ta in tas:
            self.variables[ta] = 1

        #Initializing all the courses to the number of TAs required
        for course in inp.getCourseTime().keys():
            self.assignee[course] = self.courseTACount[course]


    def addToAssignment(self, ta, assignment,value):
        """
        This function adds a new assignment i.e TA and the corresponding course
        :param ta: TA name
        :param assignment: Course name
        :param value: Amount of course to be assigned to the TA
        :return: The amount of the course assigned
        """
        if self.variables[ta] == 0:
            return 0

        val=min(self.variables[ta],value)

        if ta in self.assignment.keys():
            self.assignment[ta].append([assignment, val])
        else:
            self.assignment[ta] = [[assignment, val]]
        self.variables[ta] -= val

        return val

    def removeFromAssignment(self, ta, assignment, val):
        """
        This function removes an assignment from the existing list
        :param ta: TA name
        :param assignment: Course name
        :param val: Amount of the course assigned to the TA
        :return: void
        """
        list = self.assignment[ta]
        list.pop()

        if len(list) != 0:
            self.assignment[ta] = list
        else:
            self.assignment.pop(ta)

        self.variables[ta]+=val

    def backtracking_search(self, var, assign):
        """
        This function performs the Backtracking search
        :param var: The dictionary of TAs
        :param assign: The dictionary of courses
        :return: True/False (True of successful assignment; False otherwise)
        """
        # Assumption is if all TAs are assigned for their Full Time availability #
        # Then it is considered as assignment complete or if all the courses have their assignment complete #

        result = False
        change = 0

        global numBSNodes
        #Check if the assignment is complete
        if self.isAssignmentComplete() == True:
            return True

        tas = copy.deepcopy(var)
        values = copy.deepcopy(assign)

        #Remove the unassigned TA from the list
        ta = tas.popitem()


        for val in values.keys():
            numBSNodes+=1
            if self.variables[ta[0]] == 0:
                return True

            if values[val] != 0 and self.constraintCheck(ta[0], val) :
                change = self.addToAssignment(ta[0], val, values[val])
                values[val] -= change
                if self.variables[ta[0]] == 0:
                    result = self.backtracking_search(tas, values)
                if result == True:
                    return True
                elif self.variables[ta[0]] == 0:
                    self.removeFromAssignment(ta[0], val, change)
                    values[val] += change

        if not self.isCourseAssignmentComplete(values.values()) and self.variables[ta[0]] == 1:
            return False

        if self.isCourseAssignmentComplete(values.values()):
            return True

        if self.variables[ta[0]] == 0.5:

            #This is a partial assignment for the TA

            ret = self.backtracking_search(tas, values)
            if ret == True:
                return True
            else:
                self.removeFromAssignment(ta[0], val, change)
                values[val] += change
                return False

    def checkIfTAIsFree(self, ta, course):
        """
        This function checks if the TA is available during the course hours
        :param ta: TA name
        :param course: Course name
        :return: True/False
        """

        courseTimings = self.inp.getCourseTime()[course]

        lenTimings = len(courseTimings)

        if lenTimings%2 != 0:
            sys.exit(-1)

        numTimings = lenTimings/2

        responsibilities = self.inp.getTAResponsibilities()[ta]

        isSame = 0

        for i in range(0,numTimings):
            if courseTimings[i*2] == responsibilities[0]:
                isSame = 1
                break

        if isSame != 1:
            return True

        taClassTime = self.timeToNum(responsibilities[1])

        for i in range(0,numTimings):
            if courseTimings[i*2] == responsibilities[0]:
                courseTime = self.timeToNum(courseTimings[i*2+1])

                if not self.timeRangeCheck(courseTime,taClassTime,self.classTime,self.classTime):
                    return False

        return True


    def constraintCheck(self, ta, course):
        """
        This function checks if an assignment satisfies all the given constraints
        :param ta: TA name
        :param course: Course name
        :return: True/False
        """

        # Check if TA has all the required skills #
        if not self.skillTest(ta, course): return False

        # Check if TA has to attend the class/recitation.
        # If yes ,check if TA Class timings don't overlap with the with Course Recitation timings
        # Also, the TA has to be free during the class timings #

        if self.isTARequiredToAttendClass(course):
            if not self.recitationConstraintCheck(ta, course): return False

            return self.checkIfTAIsFree(ta, course)

        return True


    def forward_checking(self,variables,domain):
        """
        This function performs backtracking search with forward checking
        :param variables: The dictionary of TAs
        :param domain: The dictionary of courses
        :return: True/False (True of successful assignment; False otherwise)
        """
        # Assumption is if all TAs are assigned for their Full Time availability #
        # Then it is considered as assignment complete or if all the courses have their assignment complete #

        result = False
        global numFCNodes
        #Check if the assignment is complete

        if self.isAssignmentComplete() == True:
            return True

        tas = copy.deepcopy(variables)
        values = copy.deepcopy(domain)

        #Remove the unassigned TA from the list
        ta = tas.popitem()

        for val in values.keys():
            numFCNodes+=1
            if self.variables[ta[0]] == 0:
                return True
            if values[val]!=0 and self.constraintCheck(ta[0], val):
                change = self.addToAssignment(ta[0], val,values[val])
                values[val] -= change

                if(values[val]==0):
                    values.pop(val)

                if self.variables[ta[0]] == 0:
                    result = self.forward_checking(tas, values)
                if result == True:
                    return True
                elif self.variables[ta[0]] == 0:
                    self.removeFromAssignment(ta[0], val, change)

                    if val not in values:
                        values[val]=change
                    else:
                        values[val]+=change


        if not self.isCourseAssignmentComplete(values.values()) and self.variables[ta[0]] == 1:
            return False

        if self.isCourseAssignmentComplete(values.values()):
            return True

        if self.variables[ta[0]] == 0.5:
            #This is a partial assignment for the TA

            ret = self.forward_checking(tas, values)
            if ret == True:
                return True
            else:
                self.removeFromAssignment(ta[0], val, change)
                if val not in values:
                        values[val]=change
                else:
                        values[val]+=change

                return False


if __name__ == '__main__':

    print ("=======Constraint Propagation=======")

    obj = CSP()

    #obj.updateValues('testInput1')
    obj.updateValues('Test_Input_Files/testInput2')
    # obj.updateValues('testInput3')

    print "Variables : ", obj.variables,"\n"
    print "Domains: ", obj.assignee, "\n"

    # startTimeBT=timeit.default_timer() # The time when the backtracking search starts its execution
    # ret = obj.backtracking_search(obj.variables, obj.assignee)
    # endTimeBT=timeit.default_timer() # The time when the backtracking search ends its execution
    # runTimeBT=endTimeBT-startTimeBT
    # print "Total number of nodes expanded for Backtracking Search:",numBSNodes
    # print "Total time taken by the backtracking search algorithm:",runTimeBT," seconds"
    startTimeFC=timeit.default_timer() # The time when the backtracking search starts its execution
    ret=obj.forward_checking(obj.variables,obj.assignee)
    endTimeFC=timeit.default_timer() # The time when the backtracking search ends its execution
    runTimeFC=endTimeFC-startTimeFC
    print "Total number of nodes expanded for Backtracking Search with Forward Checking:",numFCNodes
    print "Total time taken by the Forward checking algorithm:",runTimeFC," seconds"

    if ret == False:
        print "Complete Assignment failed. Only partial assignment done.!\n"

    print "Assignment:",obj.assignment

