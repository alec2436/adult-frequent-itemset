import numpy as np
from Node import Node

class Tree:
    """
    Class tree will provide a tree as well as utility functions.
    the name here will be the name of the frequent itemset
    """

    def createNode(self,parent,left, name):
        """
        Utility function to create a node.
        """
        return Node(parent, left, name)

    def createRoot(self):
        node = Node(None,None, "root")
        node.count = 0
        return node

    def insert_link(self, nodebase, nodeinserted):
        # used to create item header table with custom node link
        # apparently this implements as a stack, weird
        if nodebase.next == None:
            nodebase.next = nodeinserted
            return nodeinserted
        return self.insert_link(nodebase.next, nodeinserted)

    def add(self, node, name): # either adds a node or increases the count
        if node.name == name:
            node.count += 1
            return node

        if node.down == None:
            node.down = self.createNode(node,None,name)
            return node.down

        if self.checkNextLevel(node.down, name):
            return self.findNextLevel(node.down, name)
        else:
            return self.addNextLevel(node.down, name)

    def findNextLevel(self, node, name):
        # since that itemset is in this level, it increments that node's count by one
        # then it returns that node

        if node == None:
            print "self.checkNextLevel() is wrong"

        if node.name == name:
            node.count += 1
            return node

        return self.findNextLevel(node.right, name)

    def checkNextLevel(self, node, name): # returns true if the name is in the next level of the tree
        if node == None:
            return False
        if node.name == name:
            return True
        return self.checkNextLevel(node.right,name)

    def addNextLevel(self, node, name):
        # since this node needs to be added to the next level, it checks if it's at the end of this level
        # if it is at the end it creates a new node to right
        # else it goes to the next node to the right

        if node.right == None:
            node.right = self.createNode(node.parent,node, name)
            return node.right
        
        return self.addNextLevel(node.right, name)

    def get_parents(self, node, parents_array):
        if node.parent == None: # if it's at the root node
            return parents_array
        parents_array = np.append(parents_array, node.name)
        return self.get_parents(node.parent, parents_array)

    def get_root(self, node):
        if node.parent == None:
            return node
        return self.get_root(node.parent)

    def check_single_path(self, node):
        if node == None:
            return True
        if node.right != None:
            return False
        return self.check_single_path(node.down)

    def traverse(self, node):
        if node == None:
            return node
        print node.name + " " + str(node.count)
        self.traverse(node.right)
        self.traverse(node.down)

    def traverse_diagnostics(self, node):
        if node == None:
            print "end"
            return node
        if (node.down == None) & (node.right == None):
            print node.name + " " + str(node.count) + " leaf"
            return node
        else:
            print node.name + " " + str(node.count)
        
        if node.right != None:
            self.traverse_diagnostics(node.right)
        print node.name + " " + str(node.count) + " down"
        self.traverse_diagnostics(node.down)