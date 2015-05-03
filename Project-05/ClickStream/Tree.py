__author__ = 'sri'


class Node:
        def __init__(self,val):
            self.value = val
            self.children = []
            self.parent = None

class Tree:

        def __init__(self):
            self.root = None

        def createTree(self,val):

            if self.root == None:
                print "No root"
                self.root = Node(val)
                print "Root val:",self.root.value
            else:
                self.root.children.append(val)