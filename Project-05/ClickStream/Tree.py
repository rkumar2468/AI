__author__ = 'sri'

class Node:
        def __init__(self, val):
            self.value = val
            self.children = []
            self.distribution = []
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

        def getParent(self):
            return self.parent

        def getValue(self):
            return self.value

class TreeTraversals:
       def __init__(self, node):
           self.curr = node

       def getParentList(self):
           temp = self.curr
           list = []
           while temp.getParent() != None:
             temp = temp.getParent()
             list.append(temp.value)

           return list

       def dfs(self):
           if self.curr:
                self.dfsUtil(self.curr)

       def dfsUtil(self, node):
            print node.getValue(), ' -> ',
            for i in node.getChildren():
                self.dfsUtil(i)
                print ','
            print " //"


