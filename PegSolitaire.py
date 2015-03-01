import copy
import sys
import time

import classes
import PrioQueue
import Heuristics
import ReadInput


class PegSolitaire:
    """
    Class: PegSolitaire
    This class is for playing the Peg Solitaire game based on the current configuration.
    Based on the moves, if the next configuration reaches the goal state - the player wins.
    """
    def __init__(self, startState):
        print "Game: Peg Solitaire"
        # startState = [['-','-','0','0','0','-','-'],['-','-','0','X','0','-','-'],['0','0','X','X','X','0','0'],['0','0','0','X','0','0','0'],['0','0','0','X','0','0','0'],['-','-','0','0','0','-','-'],['-','-','0','0','0','-','-']]
        self.startState = startState
        # self.goalState =  [['-','-','0','0','0','-','-'],['-','-','0','0','0','-','-'],['0','0','0','0','0','0','0'],['0','0','0','X','0','0','0'],['0','0','0','0','0','0','0'],['-','-','0','0','0','-','-'],['-','-','0','0','0','-','-']]
        self.goalState =  [[['-','-','0','0','0','-','-'],['-','-','0','0','0','-','-'],['0','0','0','0','0','0','0'],['0','0','0','X','0','0','0'],['0','0','0','0','0','0','0'],['-','-','0','0','0','-','-'],['-','-','0','0','0','-','-']],
                           [['-','-','0','0','0','-','-'],['-','-','0','0','0','-','-'],['0','0','0','0','0','0','0'],['0','0','0','X','0','0','0'],['0','0','0','0','0','0','0'],['-','-','0','0','0','-','-'],['-','-','0','0','0','-','-']]]
        self.fringeList = []
        # self.visitedList = []
        self.expandedList = []
        self.win = 0
        self.level = 0
        # self.state = 0
        self.countNodesVisited = 0
        self.MaxLevel = self.getPegsCount(startState)
        self.prioQ = PrioQueue.PrioQueue()

    def getPegsCount(self, config):
        count = 0
        for list in config:
            for element in list:
                if element == 'X':
                    count += 1
        return count

    def printExpandedList(self):
        print "!===============!"
        for config in self.expandedList:
            self.printSolitaire(config)
            print "!===============!"

    def printSolitaire(self, config):
        for row in config:
            print '  %s %s %s %s %s %s %s' %(row[0], row[1], row[2], row[3], row[4], row[5], row[6])

    def exitCondition(self):
        if self.level >= self.MaxLevel:
            print "Solution doesnot exists for the given input configuration.!"
            sys.exit(-1)

    def isConfigPresentinFringeList(self, config):
        for list in self.fringeList:
            if config == list.getList():
                return True
        return False

    def genFringeList(self, configuration, row, col, level, dfs):
        if row < 7 and col >= 2 and col < 9:    # <-- Left
            if configuration[row][col-1] == 'X' and configuration[row][col-2] == '0':
                config = []
                config = copy.deepcopy(configuration)
                config[row][col] = '0'
                config[row][col-1] = '0'
                config[row][col-2] = 'X'
                if dfs == 1:
                    if not self.isConfigPresentinFringeList(config):
                            self.fringeList.append(classes.FringeList(level,config))
                else:
                    if not self.prioQ.isConfigPresent(config):
                        priority = 0
                        heur = Heuristics.Heuristics(config)
                        if dfs == 2:
                            priority = heur.heuristics1()
                        else:
                            priority = heur.heuristics2()
                        self.prioQ.push(config,priority)
                # return
        if row < 7 and col >= 0 and col < 5:  # --> Right
            if configuration[row][col+1] == 'X' and configuration[row][col+2] == '0':
                config = []
                config = copy.deepcopy(configuration)
                config[row][col] = '0'
                config[row][col+1] = '0'
                config[row][col+2] = 'X'
                if dfs == 1:
                    if not self.isConfigPresentinFringeList(config):
                            self.fringeList.append(classes.FringeList(level,config))
                else:
                    if not self.prioQ.isConfigPresent(config):
                        priority = 0
                        heur = Heuristics.Heuristics(config)
                        if dfs == 2:
                            priority = heur.heuristics1()
                        else:
                            priority = heur.heuristics2()
                        self.prioQ.push(config,priority)
                # return
        if col < 7 and row >= 2 and row < 9:  # /\ Up
            if configuration[row-1][col] == 'X' and configuration[row-2][col] == '0':
                config = []
                config = copy.deepcopy(configuration)
                config[row][col] = '0'
                config[row-1][col] = '0'
                config[row-2][col] = 'X'
                if dfs == 1:
                    if not self.isConfigPresentinFringeList(config):
                            self.fringeList.append(classes.FringeList(level,config))
                else:
                    if not self.prioQ.isConfigPresent(config):
                        priority = 0
                        heur = Heuristics.Heuristics(config)
                        if dfs == 2:
                            priority = heur.heuristics1()
                        else:
                            priority = heur.heuristics2()
                        self.prioQ.push(config,priority)
                # return
        if col < 7 and row >= 0 and row < 5:  # \/ Down
            if configuration[row+1][col] == 'X' and configuration[row+2][col] == '0':
                config = []
                config = copy.deepcopy(configuration)
                config[row][col] = '0'
                config[row+1][col] = '0'
                config[row+2][col] = 'X'
                if dfs == 1:
                    if not self.isConfigPresentinFringeList(config):
                            self.fringeList.append(classes.FringeList(level,config))
                else:
                    if not self.prioQ.isConfigPresent(config):
                        priority = 0
                        heur = Heuristics.Heuristics(config)
                        if dfs == 2:
                            priority = heur.heuristics1()
                        else:
                            priority = heur.heuristics2()
                        # print "Priority : ", priority
                        self.prioQ.push(config,priority)
                # return

    def genValidStates(self, config, level, dfs):
        # for row in config:
        # for i in range(7):
        #     for j in range(7):
        #         print config[i][j]
        """
        :param config, level, dfs:
        :return void:
        This function is to generate all the valid states based on the current configuration/state
        """
        curr = []
        rcnt = 0
        curr.extend(config)
        # self.fringeList= []
        self.level += 1
        if curr not in self.expandedList:
            # self.expandedList.append(curr)
            for row in curr:
                ccnt = 0
                # print row
                if 'X' in row:
                    for i in row:
                        if i == 'X':
                            self.genFringeList(curr,rcnt,ccnt,self.level, dfs)
                        ccnt += 1
                rcnt += 1
        # self.printFringeList()

    def getStartState(self):
        return self.startState

    def getNextState(self):
        # print fringeList
        return self.fringeList.pop(0)    # For time being its a simple FCFS - Queue
        # if state not in expandedList:
        #     expandedList.append(state)

    def getFringeList(self):
        return self.fringeList;

    def resetLevels(self):
        self.fringeList = []
        self.state = 0
        self.level = 0
        if self.isWin():
            self.printExpandedList()
            self.printSolitaire(self.startState)
            print "!===============!"
        # print "Expanded List Count: ", len(self.expandedList)
        if self.expandedList:
            self.startState = copy.deepcopy(self.expandedList.pop(0))
        self.expandedList = []
        self.prioQ.cleanQueue()

    def printFringeList(self):
        temp = 0
        print "Printing Fringe List: "
        while temp < len(self.fringeList):
            self.printSolitaire(self.fringeList[temp].getList())
            temp += 1
            print

    def isWin(self):
        return self.win

    def playGame1(self, dfs, level):
        # Generating the Valid states (children of the current state).
        # nextState=[]
        # if self.state > self.level:
            # Level Reached. Just dont generate any successors for the elements.
            # Instead store the current fringeList to some other variable.

            # Resetting everything and increasing the level ans starting again.
            # self.resetLevels()
            # self.level += 1
        # elif self.state < self.level:
       # self.state += 1
        # self.printSolitaire(self.startState)
        if self.startState in self.goalState:
            self.printSolitaire(startState)
            print "\n You Won the game.!"
            self.fringeList=[]
            self.expandedList=[]
            self.win = 1
        elif dfs == 1:
            # Play using Iterative Deepening Search or DFS
            # print
            if self.level < level:
                self.genValidStates(self.startState, level, dfs)
            if self.level == 0:
                self.countNodesVisited += 1 # For the start state visit
            while True:
                if not self.fringeList:
                    break
                self.countNodesVisited += 1
                # print "Adding the below state to expanded list:"
                self.expandedList.append(self.startState)
                self.startState = []
                fringe = self.getNextState()
                self.startState = fringe.getList()
                curLevel = fringe.getLevel()
                if self.startState in self.goalState:
                    # self.printSolitaire(self.startState)
                    print "\n You Won the game.!"
                    self.fringeList=[]
                    self.win = 1
                    return
                else:
                    self.level = curLevel
                    self.playGame(dfs, level)
                    break
                # self.printSolitaire(self.getNextState())
                # print
                # print '======================'
                # print
            # self.level += 1
        else:
            # print "\n Playing with A* configuration. ", self.countNodesVisited
            self.genValidStates(self.startState,level,dfs)
            while True:
                if self.prioQ.isEmpty():
                    break
                self.countNodesVisited += 1
                # print "Adding the below state to expanded list:"
                self.expandedList.append(self.startState)
                self.startState = []
                fringe = self.prioQ.getMin()
                self.startState = fringe[1]
                if self.startState in self.goalState:
                    # self.printSolitaire(self.startState)
                    print "\n Congratulations. You Won the game.!"
                    self.prioQ.cleanQueue()
                    self.win = 1
                    return
                else:
                    self.playGame(dfs, level)
                    break

    def playGame(self, dfs, level):
        # Generating the Valid states (children of the current state).
        # nextState=[]
        # if self.state > self.level:
            # Level Reached. Just dont generate any successors for the elements.
            # Instead store the current fringeList to some other variable.

            # Resetting everything and increasing the level ans starting again.
            # self.resetLevels()
            # self.level += 1
        # elif self.state < self.level:
       # self.state += 1
        # self.printSolitaire(self.startState)
        if self.startState in self.goalState:
            self.printSolitaire(startState)
            print "\n You Won the game.!"
            self.fringeList=[]
            self.expandedList=[]
            self.win = 1
        elif dfs == 1:
            # Play using Iterative Deepening Search or DFS

            # print
            while True:
                if self.level < level:
                    self.genValidStates(self.startState, level, dfs)
                if self.level == 0:
                    self.countNodesVisited += 1 # For the start state visit

                if not self.fringeList:
                    break
                self.countNodesVisited += 1
                # print "Adding the below state to expanded list:"
                self.expandedList.append(self.startState)
                self.startState = []
                fringe = self.getNextState()
                self.startState = fringe.getList()
                curLevel = fringe.getLevel()
                if self.startState in self.goalState:
                    # self.printSolitaire(self.startState)
                    print "\n You Won the game.!"
                    self.fringeList=[]
                    self.win = 1
                    return
                else:
                    self.level = curLevel
                    # self.playGame(dfs, level)
                    # break
                # self.printSolitaire(self.getNextState())
                # print
                # print '======================'
                # print
            # self.level += 1
        else:
            # print "\n Playing with A* configuration. ", self.countNodesVisited
            while True:
                self.genValidStates(self.startState,level,dfs)
                if self.prioQ.isEmpty():
                    break
                self.countNodesVisited += 1
                # print "Adding the below state to expanded list:"
                self.expandedList.append(self.startState)
                self.startState = []
                fringe = self.prioQ.getMin()
                self.startState = fringe[1]
                if self.startState in self.goalState:
                    # self.printSolitaire(self.startState)
                    print "\n Congratulations. You Won the game.!"
                    self.prioQ.cleanQueue()
                    self.win = 1
                    return
                # else:
                    # self.playGame(dfs, level)
                    # break
                    # continue

    def gameStat(self):
        print "-- Number of nodes Visited: %d" %(self.countNodesVisited)

if __name__ == '__main__':
    # startState = [['-','-','X','X','X','-','-'],['-','-','X','X','X','-','-'],['0','0','X','X','X','0','0'],['0','0','X','0','X','0','0'],['0','0','0','0','0','0','0'],['-','-','0','0','0','-','-'],['-','-','0','0','0','-','-']]
    # startState = [['-','-','0','0','0','-','-'],['-','-','0','0','0','-','-'],['0','0','0','0','0','0','0'],['0','0','0','X','0','0','0'],['0','0','0','0','0','0','0'],['-','-','0','0','0','-','-'],['-','-','0','0','0','-','-']]
    # startState = [['-','-','0','0','0','-','-'],['-','-','0','X','0','-','-'],['0','0','X','X','X','0','0'],['0','0','0','X','0','0','0'],['0','0','0','X','0','0','0'],['-','-','0','0','0','-','-'],['-','-','0','0','0','-','-']]
    # startState = [['-','-','0','0','0','-','-'],['-','-','0','X','0','-','-'],['0','0','0','X','0','0','0'],['0','0','0','0','0','0','0'],['0','0','0','0','0','0','0'],['-','-','0','0','0','-','-'],['-','-','0','0','0','-','-']]
    # printSolitaire(startState)
    # Creating object of PegSolitaire class.

    File = ReadInput.readInput("configuration.txt")
    startState = File.getStartStateFromConfigFile()
    # print startState
    # print
    # print startState1

    game = PegSolitaire(startState)
    # game.printSolitaire(startState)
    i = 0
    print "Algorithm to be used: \n 1. I-DFS \n 2. A* - Heuristic - I \n 3. A* - Heuristic - II "
    choice = input()
    if  choice == '' or not (choice >= 1 and choice <= 3):
        print "Wrong Choice.!"
        sys.exit(-1)
    timeStart = time.time()
    if choice == 1:
        # IDFS #
        while True:
            game.playGame(1,i)
            game.exitCondition()
            game.resetLevels()
            game.gameStat()
            # print "Level: %d" %(i)
            i += 1
            if game.isWin() == 1:
                break
        # game.gameStat()
    else:
        # A* #
        game.playGame(choice,0)
        game.resetLevels()
        game.gameStat()
        if game.isWin() == 0:
            print "\n Solution doesnot exists for the given input configuration.!"
    timeDiff = time.time() - timeStart
    print "Time taken for ",
    if choice == 1:
        print "IDFS: ", timeDiff
    elif choice == 2:
        print "A* Heuristic 1: ", timeDiff
    else:
        print "A* Heuristic 2: ", timeDiff