import copy, sys
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
        self.inValidAssign=[]

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
            print "In is Assignment complete; self.assignee.values:",self.assignee.values
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

    def addToAssignment(self, ta, assignment,value):
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
        list = self.assignment[ta]
        x= list.pop() # Need to check if the pop is doing last updated value - Yes it is updated.

        if len(list) != 0:
            self.assignment[ta] = list
        else:
            self.assignment.pop(ta)

        self.variables[ta]+=val

    def backtracking_search(self, var, assign):
        # Assumption is if all TAs are assigned for their Full Time availability #
        # Then it is considered as assignment complete or if all the courses have their assignment complete #
        result = False
        change = 0
        if self.isAssignmentComplete() == True:
            #print "Assignment is complete"
            return True
        tas = copy.deepcopy(var)
        values = copy.deepcopy(assign)
        # while len(tas) != 0:
        ta = tas.popitem()
        for val in values.keys():
            if self.variables[ta[0]] == 0:
                return True
            # Added extra condition to eliminate already completed assignments #
            if values[val] != 0 and self.constraintCheck(ta[0], val) :
                # values.pop(val)
                change = self.addToAssignment(ta[0], val, values[val])
                values[val] -= change
                if self.variables[ta[0]] == 0:
                    print "Entering Recursion from ", ta[0], " with ",tas, values
                    result = self.backtracking_search(tas, values)
                if result == True:
                    print "Returning true from ", ta[0], " with ",tas, val
                    return True
                # Problem is here - Resolved #
                elif self.variables[ta[0]] == 0:
                    self.removeFromAssignment(ta[0], val, change)
                    values[val] += change
                    print "Removing entries due to failure at ", ta[0], " with ",tas, val," Curr Val: ", values

        if not self.isCourseAssignmentComplete(values.values()) and self.variables[ta[0]] == 1:
            print "For loop exhausted for ", ta[0]
            return False

        if self.isCourseAssignmentComplete(values.values()):
            return True

        print "Returning False after no assignment to ", ta[0], values
        if self.variables[ta[0]] == 0.5:
            """
            This is essentially a partial assignment
            """
            ret = self.backtracking_search(tas, values)
            if ret == True:
                return True
            else:
                # Remove self.variable entry #
                # Update values (optional) #
                # return false #
                self.removeFromAssignment(ta[0], val, change)
                values[val] += change
                return False

    def checkIfTAIsFree(self, ta, course):
        courseTimings = self.inp.getCourseTime()[course]

        # Need to revisit #
        if len(courseTimings)%2 != 0:
            #print "Course Timings Error for the course: ", course
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
        # Check if TA has to attend the class, # if yes ,Check if TA Class timings doesnt class with Course Recitations
        # TA has to be free during the class timings #
        if self.isTARequiredToAttendClass(course):
            if not self.recitationConstraintCheck(ta, course): return False

            return self.checkIfTAIsFree(ta, course)

        # If the control comes here, all the Cases are passed #
        return True


    def forward_checking(self,variables,domain):
        # Assumption is if all TAs are assigned for their Full Time availability #
        # Then it is considered as assignment complete or if all the courses have their assignment complete #
        result = False
        if self.isAssignmentComplete() == True:
            #print "Assignment is complete"
            return True
        tas = copy.deepcopy(variables)
        values = copy.deepcopy(domain)
        while len(tas) != 0:
            ta = tas.popitem()
            for val in values.keys():
                if self.variables[ta[0]] == 0:
                    return True
                #print "Before Constraint check:",ta[0],val
                # Added extra condition to eliminate already completed assignments #
                if values[val]!=0 and self.constraintCheck(ta[0], val):
                    # values.pop(val)
                    change = self.addToAssignment(ta[0], val,values[val])
                    #print "Retval in BT:",change
                    #print "Assignment:",ta[0],val
                    values[val] -= change
                    #print "Value of val:",values[val]
                    if(values[val]==0):
                        values.pop(val)
                    #print "Values in forward checking:",values
                    if self.variables[ta[0]] == 0:
                        result = self.forward_checking(tas, values)
                    if result == True:
                        # print "Assignment Succeeded.!"
                        return True
                    # Problem is here #
                    elif self.variables[ta[0]] == 0:
                        self.removeFromAssignment(ta[0], val, change)
                        # The popped value is being added at the end; don't know if it will be a problem
                        values[val]=change
                        #print "Values after replacing the val:",values

        # temp = values
        if self.isCourseAssignmentComplete(values.values()):
            return True
        return False


if __name__ == '__main__':
    print ("Testing CSP.!")
    obj = CSP()
    obj.updateValues('Sai_Input')
    # obj.updateValues('dataset_AI_CSP')
    # obj.updateValues('testInput')
    # obj.updateValues('testInput2')
    # print obj.assignee
    # print "Variables : ", obj.variables
    print
    # print "Assignees: ", obj.assignee, "\n"
    ret = obj.backtracking_search(obj.variables, obj.assignee)
    #ret=obj.forward_checking(obj.variables,obj.assignee)
    if ret == False:
        print "Complete Assignment failed. Only partial assignment done.!\n"

    print "Assignment:",obj.assignment
    # f=open('test.txt','w')
    # for keys in obj.assignment.keys():
    #     print >> f, "Key - ", keys, " Val: ", obj.assignment[keys], "\n"
    # f.close()
    # obj.forward_checking(obj.variables,obj.assignee)
    # print obj.courseTACount
