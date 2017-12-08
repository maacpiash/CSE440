# Md. Abdul Ahad Chowdhury
# ID: 1410575042
# CSE440.1, Fall 2017

""" Attributes start from 0, but classes start from 1 """

import sys, math, random

global_option = None    # {"optimized", "randomized", "forest3", "forest15"}
pruning_thr = 50        # Pruning Threshold
attrList = []           # List of attributes


""" Node class """
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
    # END OF NODE CLASS

""" DTL functions """

# Decision Tree Learning
def DTL(examples, attributes, default, treeID, nodeID):
    # returns a decision tree
    print("DTL call: treeID = %2d, nodeID = %3d" % (treeID, nodeID))
    if len(examples) <= pruning_thr: # Not enough exapmles to consider
        print("Examples ran out.")
        if global_option == "optimized":
            return default.index(max(default))
        else:
            return default
    if homogeneous(examples): # All the examples have the same class
        print("Homogeneous examples.")
        return examples[0][1]
    # Base cases completed
    if global_option == "optimized":
        best_attribute, best_threshold, max_gain = CHOOSE_ATTRIBUTE(examples, attributes)
    else:
        best_attribute, best_threshold, max_gain = RANDOM_ATTRIBUTE(examples, attributes)
    tree = Node(treeID, nodeID, best_attribute, best_threshold, max_gain)
    examples_left, examples_right = seperate(examples, best_attribute, best_threshold)
    newID = nodeID * 2
    tree.left_child = DTL(examples_left, attributes, DISTRIBUTION(examples), treeID, newID)
    tree.right_child = DTL(examples_right, attributes, DISTRIBUTION(examples), treeID, newID + 1)
    return tree

def DISTRIBUTION(examples):
    # returns a probability vector according to examples
    totalSamples = len(examples)
    classList = getClasses(examples)
    totalClasses = len(classList)
    distribution = [float(0)] * (totalClasses + 1)
    for sample in examples:
        distribution[sample[1]] = ((distribution[sample[1]] * totalSamples) + 1) / totalSamples
    return distribution
        
def homogeneous(examples):
    # returns true if each sample in examples is of the same class
    if len(examples) == 1:
        return True
    firstClass = examples[0][1]
    for sample in examples:
        if sample[1] != firstClass:
            return False
    return True

def CHOOSE_ATTRIBUTE(examples, attributes):
    # chooses the attribute and the threshold for it that give the best information gain
    max_gain = best_attribute = best_threshold = -1
    for a in attributes:
        attribute_values = SELECT_COLUMN(examples, a)
        L, M = min(attribute_values), max(attribute_values)
        for K in range(1, 51):
            threshold = L + K * (M - L) / 51
            gain = INFORMATION_GAIN(examples, a, threshold)
            if gain > max_gain:
                max_gain, best_attribute, best_threshold = gain, a, threshold
    return best_attribute, best_threshold, max_gain

def RANDOM_ATTRIBUTE(examples, attributes):
    # chooses a random attribute and the threshold for that give the best information gain
    max_gain = best_attribute = best_threshold = -1
    a = random.choice(attributes)
    attribute_values = SELECT_COLUMN(examples, a)
    L, M, K = min(attribute_values), max(attribute_values), 1
    while K <= 50:
        threshold = L + K * (M - L) / 51
        gain = INFORMATION_GAIN(examples, a, threshold)
        if gain > max_gain:
            max_gain, best_threshold = gain, threshold
        K += 1
    return best_attribute, best_threshold, max_gain

def SELECT_COLUMN(examples, attribute):
    # returns a list of values of the particular attribute among examples
    values = []
    for sample in examples:
        values.append(sample[0][attribute])
    return values

def INFORMATION_GAIN(examples, attribute, threshold):
    # returns the information gain of a node considering some examples,
    # one of their attributes and a certain threshold for that attribute
    root_entropy = ENTROPY(frequency(examples))
    K = len(examples)
    leftChildren, rightChildren = seperate(examples, attribute, threshold)
    left_weight, right_weight = len(leftChildren) / K, len(rightChildren) / K
    left_entropy, right_entropy = ENTROPY(frequency(leftChildren)), ENTROPY(frequency(rightChildren))
    return root_entropy - left_weight * left_entropy - right_weight * right_entropy

def seperate(examples, attribute, threshold):
    # seperates the "examples" based on "attribute" by its "threshold"
    lList, rList = [], []
    for sample in examples:
        if sample[0][attribute] < threshold:
            lList.append(sample)
        else:
            rList.append(sample)
    return lList, rList

def ENTROPY(numbers):
    # returns a float, H, which is the entropy of "numbers"
    # "numbers" is a list of integers that represent how many items each class has
    # i.e. "numbers[c] = f" means that "f number of samples is of class c"
    K = sum(numbers)        
    H = 0
    for Ki in numbers:
        ratio = Ki / K
        if int(ratio) != 0:
            H -= ratio * math.log2(ratio)
    return H

def frequency(examples):
    # returns a list of integers, which represent how many items in examples each class has
    # i.e. "freq[c] = f" means that "f number of sample(s) in examples is of class c"
    freq = [0] * (numberOfClasses + 1)
    for sample in examples:
        freq[sample[1]] += 1
    return freq

def getClasses(examples):
    # returns a list of classes
    classList = []
    for sample in examples:
        i = sample[1]
        if i not in classList:
            classList.append(i)
    return classList


"""
    ##### The procedure of the program starts here #####
"""


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
    tupl = (attrRow, cIass)
    # Each example data is saved as a tuple in (attribute_array, class) format
    examples.append(tupl)

# print(str(type(examples)))            #  => list       of tuples    
# print(str(type(examples[0])))         #  => tuple      of (list_of_float, int)
# print(str(type(examples[0][0])))      #  => list       of float
# print(str(type(examples[0][0][0])))   #  => float

for i in range(len(examples[0][0])):
    attrList.append(i)
numberOfClasses = len(getClasses(examples))

if global_option in {"optimized", "randomized"}:
    tree = DTL(examples, attrList, DISTRIBUTION(examples), 0, 1)
    tree.Console_WriteLine()
else:
    forest = [] # Array of trees
    numTrees = 3 if global_option == "forest3" else 15
    for i in range(numTrees):
        tree = DTL(examples, attrList, DISTRIBUTION(examples), i, 1)
        forest.append(tree)
    for tree in forest:
        tree.Console_WriteLine()