class FringeList:
    """
    Class: FringeList
    This is an implementation of fringe list datastructure for the Peg Solitaire game.

    Functions:
        getLevel - Returns the level of the current configuration
        getList - returns the current Fringe List
    """
    def __init__(self, level, list):
        self.level = level
        self.list = list

    def getLevel(self):
        return self.level
    def getList(self):
        return self.list
