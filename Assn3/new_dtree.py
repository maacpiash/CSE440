import sys


""" Sample class defn"""
class Sample:
    def __init__(self, attributes, klass):
        self.attributes = attributes
        self.klass = klass
""" End of Sample class defn"""

""" Node class defn"""
class Node:
    # START OF NODE CLASS
    def __init__(self, treeID, nodeID, featID, threshold, infoGain):
        self.treeID = treeID
        self.nodeID = nodeID
        self.featID = featID
        self.threshold = threshold
        self.infoGain = infoGain
        self.left_child = self.right_child = None
    
    def Console_WriteLine(self):
        # An homage to C# (^_^)
        q = []
        # Implementing basic DFS by a queue data structure
        q.append(self)
        while len(q) > 0: 
            node = q.pop()       
            print("tree=%2d, node=%3d, feature=%2d, thr=%6.2lf, gain=%lf" % (node.treeID, node.nodeID, node.featID, node.threshold, node.infoGain))
            if type(node.left_child) is Node:
                q.append(node.left_child)
            else:
                print(str(node.left_child))
            if type(node.right_child) is Node:
                q.append(node.right_child)
            else:
                print(str(node.right_child))
""" End of Node class defn"""
        


""" Programm process """

try:
    training_file, test_file, global_option = sys.argv[1:4]
except:
    print("ERROR : Invalid number of arguments.")
    sys.exit()

if global_option not in {"optimized", "randomized", "forest3", "forest15"}:
    print("ERROR : Invalid Option.")
    print('Option must be "optimized", "randomized", "forest3" or "forest15".')
    sys.exit()

# This is the list that would contain all the sample data
examples = []

# The list of all lines in the files
training_lines, test_lines = [], []

# File I/O
try:
    with open(training_file, 'r') as f:
        training_lines = f.readlines() # took all the lines in a list of strings
except:
    print("ERROR : Training file could not be opened.")
    sys.exit()

try:
    with open(test_file, 'r') as f:
        test_lines = f.readlines() # took all the lines in a list of strings
except:
    print("ERROR : Test file could not be opened.")
    sys.exit()

if training_lines[-1] != '\n':
    # Adding a carraige return at the end of the last line, for convenience
    training_lines[-1] = training_lines[-1] + '\n'

# Processing the lines read from the file as attributes and class
for oneExample in training_lines:
    attributes = oneExample.split()
    attrRow = []
    for attr in attributes[:-1]:
        attrRow.append(float(attr))
    cIass = int(oneExample[-2])
    examples.append(Sample(attrRow, cIass))