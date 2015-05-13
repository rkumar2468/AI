__author__ = 'sri'

class Node: #This class represents the tree data structure
        def __init__(self, val):
            self.value = val
            self.children = []
            self.distribution = 0
            self.parent = None

        def addDist(self, dist):
            self.distribution = dist

        def addChildren(self, childNode):
            if self.children:
                self.children.append(childNode)
            else:
                self.children = [childNode]
            childNode.parent = self

        def getChildren(self):
            return self.children

        def getDistribution(self):
            return self.distribution

        def getParent(self):
            return self.parent

        def getValue(self):
            return self.value

class TreeTraversals:
       def __init__(self, node):
           self.root = node

       def getParentList(self): #Function to get the parents of a given node
           temp = self.root
           list = []
           while temp.getParent() != None:
             temp = temp.getParent()
             list.append(temp.value)

           return list

       def dfs(self):
           if self.root:
                self.dfsUtil(self.root)

       def dfsUtil(self, node):
            print node.getValue(), ' -> ',
            for i in node.getChildren():
                self.dfsUtil(i)
                print ','
            print " //"


