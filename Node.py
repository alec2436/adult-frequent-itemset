class Node:
    """
    Class Node
    """
    def __init__(self, parent,left, name):
        self.down = None # go down one level in the tree
        self.right = None # go to the right on the same level in the tree
        self.parent = parent # go to the parent (up a level)
        self.name = name # name of the itemset it represents
        self.count = 1 # count
        self.next = None # represents the next node of the SAME itemset in the tree, for the custon node link
        self.left = left # go to the left, same level but back 