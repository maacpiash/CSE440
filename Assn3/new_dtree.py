import sys, math, random

pruning_thr = 50
global_classes_count = 0
global_attribs_count = 0
global_option = None
global_classes_list = []

""" Sample class definition"""
class Sample:
    def __init__(self, attributes, Class):
        self.attributes = attributes
        self.Class = Class

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

""" Node class definition"""

class Node:
    # START OF NODE CLASS
    def __init__(self, treeID, nodeID, featID, threshold, infoGain):
        self.treeID = treeID
        self.nodeID = nodeID
        self.featID = featID
        self.threshold = threshold
        self.infoGain = infoGain
        self.left_child = None
        self.right_child = None
    
    def Console_WriteLine(self):
        q = []
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

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

""" DTL functions definition"""

def DTL(examples, default, treeID, nodeID):
    print("DTL call: treeID = %2d, nodeID = %3d" % (treeID, nodeID))
    if len(examples) < pruning_thr:
        return default
    if homogeneous(examples):
        return examples[0].Class
    if global_option == "optimized":
        best_attribute, best_threshold, max_gain = CHOOSE_ATTRIBUTE(examples)
    else:
        best_attribute, best_threshold, max_gain = RANDOM_ATTRIBUTE(examples)
    tree = Node(treeID, nodeID, best_attribute, best_threshold, max_gain)
    examples_left, examples_right = seperate(examples, best_attribute, best_threshold)
    tree.left_child = DTL(examples_left, DISTRIBUTION(examples), treeID, nodeID * 2)
    tree.right_child = DTL(examples_right, DISTRIBUTION(examples), treeID, nodeID * 2 + 1)
    return tree

def CHOOSE_ATTRIBUTE(examples):
    max_gain = best_attribute = best_threshold = -1
    for A in range(global_attribs_count):
        attribute_values = SELECT_COLUMN(examples, A)
        L, M = min(attribute_values), max(attribute_values)
        for K in range(1, 51):
            threshold = L + K * (M - L) / 51
            gain = INFORMATION_GAIN(examples, A, threshold)
            if gain > max_gain:
                max_gain, best_attribute, best_threshold = gain, A, threshold
    return best_attribute, best_threshold, max_gain

def RANDOM_ATTRIBUTE(examples):
    max_gain = best_attribute = best_threshold = -1
    A = random.randint(0, global_attribs_count - 1)
    attribute_values = SELECT_COLUMN(examples, A)
    L, M = min(attribute_values), max(attribute_values)
    for K in range(1, 51):
        threshold = L + K * (M - L) / 51
        gain = INFORMATION_GAIN(examples, A, threshold)
        if gain > max_gain:
            max_gain, best_attribute, best_threshold = gain, A, threshold
    return best_attribute, best_threshold, max_gain

def SELECT_COLUMN(examples, attribute): # OK
    aList = []
    for sample in examples:
        aList.append(sample.attributes[attribute])
    return aList

def INFORMATION_GAIN(examples, attribute, threshold): # OK
    lhs, rhs = seperate(examples, attribute, threshold)
    K1, K2 = len(lhs), len(rhs)
    K = K1 + K2
    r1, r2 = K1 / K, K2 / K
    H = ENTROPY(frequency(examples).values())
    print("Root entropy = " + str(H))
    H1, H2 = ENTROPY(frequency(lhs).values()), ENTROPY(frequency(rhs).values())
    return H - r1 * H1 - r2 * H2

def ENTROPY(frequency): # OK
    K = sum(frequency)
    H = 0
    for x in frequency:
        try:
            r = x / K
            H -= r * math.log2(r)
        except:
            H -= 0
    return H

def DISTRIBUTION(examples): # OK
    f = frequency(examples)
    d = []
    n = sum(f)
    for x in f:
        d.append(x / n)
    return d

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

""" Helper functions definition"""

def homogeneous(examples): # OK
    firstClass = examples[0].Class
    for sample in examples:
        if sample.Class != firstClass:
            return False
    return True

def seperate(examples, attribute, threshold): # OK
    l, r = [], []
    for sample in examples:
        if sample.attributes[attribute] < threshold:
            l.append(sample)
        else:
            r.append(sample)
    return l, r

def frequency(examples): # OK
    frequency = dict.fromkeys(global_classes_list)
    for c in global_classes_list:
        frequency[c] = 0
    for sample in examples:
        frequency[sample.Class] += 1
    return frequency

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

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
    if cIass not in global_classes_list:
        global_classes_list.append(cIass)
    examples.append(Sample(attrRow, cIass))

global_attribs_count = len(examples[0].attributes)
global_classes_count = len(global_classes_list)

# print("Classes = " + str(global_classes_count))
# print("Attribs = " + str(global_attribs_count))