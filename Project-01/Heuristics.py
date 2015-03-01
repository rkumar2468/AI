class Heuristics:
    """
    Class: Heuristics
    This class is for computing heuristic value based on the current configuration.
    This value tells us how close the current configuration w.r.t the goal state defined in the game.

    Members: config - contains the configuration to compute the heuristic value.
    Functions:
        heuristic1
            This computes the number of isolated pegs on the board.
            Idea: The more the isolated pegs the lesser the priority for this configuration to be selected.
                  This is a better way to decide the next configuration.
        heuristic2
            This computes the number of pairs of pegs on the board.
            Idea: The more the pairs the higher the priority for this configuration to be selected.
                  This is not optimal w.r.t. heuristic1, but it has better space optimization w.r.t IDFS.
    """
    def __init__(self, config):
        self.config = config

    def computePairs(self):
        """
        This function computes the number of pairs present in the configuration.
        :return: h :- 32 - # of pairs
        """
        h = 32
        rcnt = 0
        for row in self.config:
            ccnt = 0
            if 'X' in row:
                for i in row:
                    if i == 'X':
                        # self.genFringeList(curr,rcnt,ccnt,self.level, dfs)
                        if rcnt >= 1 and rcnt <= 5:
                            if ccnt >= 1 and ccnt <= 5:
                                if self.config[rcnt][ccnt+1] == 'X' or self.config[rcnt][ccnt-1] == 'X' and self.config[rcnt-1][ccnt] != 'X' or self.config[rcnt+1][ccnt] == 'X':
                                    h -= 1
                            elif ccnt == 0:
                                if self.config[rcnt][ccnt+1] == 'X' or self.config[rcnt-1][ccnt] == 'X' or self.config[rcnt+1][ccnt] == 'X':
                                    h -= 1
                            else:
                                if self.config[rcnt][ccnt-1] == 'X' or self.config[rcnt-1][ccnt] == 'X' or self.config[rcnt+1][ccnt] == 'X':
                                    h -= 1
                        else:
                            # Row 0
                            if rcnt == 0:
                                if ccnt >= 1 and ccnt <= 5:
                                    if self.config[rcnt][ccnt+1] == 'X' or self.config[rcnt][ccnt-1] == 'X' or self.config[rcnt+1][ccnt] == 'X':
                                        h -= 1
                                elif ccnt == 0:
                                    if self.config[rcnt][ccnt+1] == 'X' or self.config[rcnt+1][ccnt] == 'X':
                                        h -= 1
                                else:
                                    if self.config[rcnt][ccnt-1] == 'X' or self.config[rcnt+1][ccnt] == 'X':
                                        h -= 1
                            else:
                                if ccnt >= 1 or ccnt <= 5:
                                    if self.config[rcnt][ccnt+1] == 'X' or self.config[rcnt][ccnt-1] == 'X' or self.config[rcnt-1][ccnt] == 'X':
                                        h -= 1
                                elif ccnt == 0:
                                    if self.config[rcnt][ccnt+1] == 'X' or self.config[rcnt-1][ccnt] == 'X':
                                        h -= 1
                                else:
                                    if self.config[rcnt][ccnt-1] == 'X' or self.config[rcnt-1][ccnt] == 'X':
                                        h -= 1
                    ccnt += 1
            rcnt += 1
        return h

    def computePegs(self):
        """
        This function computes the number of pegs present in the configuration.
        :return: # of pegs
        """
        pegs = 0
        for list in self.config:
            for element in list:
                if element == 'X':
                    pegs += 1
        return pegs

    def heuristics1(self):
        """
        The more the isolated nodes, the lower should be the priority. Which means high h value.
        :return: heuristic value, h
        """
        h = 10
        rcnt = 0
        for row in self.config:
            ccnt = 0
            if 'X' in row:
                for i in row:
                    if i == 'X':
                        # self.genFringeList(curr,rcnt,ccnt,self.level, dfs)
                        if rcnt >= 1 and rcnt <= 5:
                            if ccnt >= 1 and ccnt <= 5:
                                if self.config[rcnt][ccnt+1] != 'X' and self.config[rcnt][ccnt-1] != 'X' and self.config[rcnt-1][ccnt] != 'X' and self.config[rcnt+1][ccnt] != 'X':
                                    h += 1
                            elif ccnt == 0:
                                if self.config[rcnt][ccnt+1] != 'X' and self.config[rcnt-1][ccnt] != 'X' and self.config[rcnt+1][ccnt] != 'X':
                                    h += 1
                            else:
                                if self.config[rcnt][ccnt-1] != 'X' and self.config[rcnt-1][ccnt] != 'X' and self.config[rcnt+1][ccnt] != 'X':
                                    h += 1
                        else:
                            # Row 0
                            if rcnt == 0:
                                if ccnt >= 1 and ccnt <= 5:
                                    if self.config[rcnt][ccnt+1] != 'X' and self.config[rcnt][ccnt-1] != 'X' and self.config[rcnt+1][ccnt] != 'X':
                                        h += 1
                                elif ccnt == 0:
                                    if self.config[rcnt][ccnt+1] != 'X' and self.config[rcnt+1][ccnt] != 'X':
                                        h += 1
                                else:
                                    if self.config[rcnt][ccnt-1] != 'X' and self.config[rcnt+1][ccnt] != 'X':
                                        h += 1
                            else:
                                if ccnt >= 1 and ccnt <= 5:
                                    if self.config[rcnt][ccnt+1] != 'X' and self.config[rcnt][ccnt-1] != 'X' and self.config[rcnt-1][ccnt] != 'X':
                                        h += 1
                                elif ccnt == 0:
                                    if self.config[rcnt][ccnt+1] != 'X' and self.config[rcnt-1][ccnt] != 'X':
                                        h += 1
                                else:
                                    if self.config[rcnt][ccnt-1] != 'X' and self.config[rcnt-1][ccnt] != 'X':
                                        h += 1
                    ccnt += 1
            rcnt += 1
        return h

    def heuristics2(self):
        """
        This function computes the pairs of pegs on the board.
        The more the pairs the lesser the priority.
        :return: heuristic value, h
        """
        h2 = self.computePairs()
        return h2