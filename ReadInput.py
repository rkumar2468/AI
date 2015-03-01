import os, sys

class readInput:
    def __init__(self, filename):
        self.file = filename
        self.list = []

    def generateStartState(self):
        if not os.path.exists(self.file):
            print "Error: File \'%s\' doesnot exists.!" %(self.file)
            sys.exit(-1)
        fid = open(self.file,'r')
        local = []
        for line in fid:
            # print line
            local = []
            for ch in line:
                if ch != '\n':
                    local.append(ch)
            self.list.append(local)
        fid.close()

    def getStartStateFromConfigFile(self):
        self.generateStartState()
        return self.list

# if __name__ == "__main__":
#     file = "configuration.txt"
#     f = readInput(file)
#     list = f.getStartStateFromConfigFile()
#     print list