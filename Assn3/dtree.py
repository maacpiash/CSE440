# Md. Abdul Ahad Chowdhury
# ID: 1410575042
# CSE440.1, Fall 2017

""" Attributes start from 0, but classes start from 1 """

import sys, math, random

numberOfClasses = 0
option = None
threshold = None

class Node:
    # START OF NODE CLASS
    def __init__(self, treeID, nodeID, featID, threshold, infoGain):
        self.treeID = treeID
        self.nodeID = nodeID
        self.featID = featID
        self.threshold = threshold
        self.infoGain = infoGain
        self.left = self.right = None
    
    def Console_WriteLine(self):
        # An homage to C# (^_^)
        q = []
        # Implementing basic DFS by a queue data structure
        node = self
        q.append(node)
        while q.__len__() > 0: 
            node = q.pop()       
            print("tree=%2d, node=%3d, feature=%2d, thr=%6.2lf, gain=%lf" % (node.treeID, node.nodeID, node.featID, node.threshold, node.infoGain))
            if node.left != None:
                q.append(node.left)
            if node.right != None:
                q.append(node.right)
    # END OF NODE CLASS

def DTL(examples, attributes, default, treeID, nodeID):
    if len(examples) <= threshold: # No more exapmle
        return default
    sameClass = homogeneous(examples) # Checks if all the examples have the same class
    if sameClass != None:
        return sameClass
    if option == "optimized":
        best_attribute, best_threshold, max_gain = CHOOSE_ATTRIBUTE(examples, attributes)
    else:
        best_attribute, best_threshold, max_gain = RANDOM_ATTRIBUTE(examples, attributes)
    tree = Node(treeID, nodeID, best_attribute, best_threshold, max_gain)
    examples_left, examples_right = [], []
    for sample in examples:
        if sample[1] < threshold:
            examples_left.append(sample)
        else:
            examples_right.append(sample)
    tree.left = DTL(examples_left, attributes, DISTRIBUTION(examples), treeID, nodeID * 2)
    tree.right = DTL(examples_right, attributes, DISTRIBUTION(examples), treeID, nodeID* (2 + 1))
    return tree

def DISTRIBUTION(examples):
    totalSamples = len(examples)
    totalClasses = max(examples, key=lambda x: x[1])[1]
    distribution = [float(0)] * totalClasses
    for sample in examples:
        distribution[sample[1]] = ((distribution[sample[1]] * totalClasses) + 1) / totalClasses
    return distribution
        
def homogeneous(examples):
    firstClass = examples.pop()[1]
    for sample in examples:
        if sample[1] != firstClass:
            return None
    return firstClass

def CHOOSE_ATTRIBUTE(examples, attributes):
    max_gain = best_attribute = best_threshold = -1
    for a in attributes:
        attribute_values = SELECT_COLUMN(examples, a)
        L, M, K = min(attribute_values), max(attribute_values), 1
        while K <= 50:
            threshold = L + K * (M - L) / 51
            gain = INFORMATION_GAIN(examples, a, threshold)
            if gain > max_gain:
                max_gain, best_attribute, best_threshold = gain, a, threshold
            K += 1
    return best_attribute, best_threshold, max_gain

def RANDOM_ATTRIBUTE(examples, attributes):
    max_gain = best_attribute = best_threshold = -1
    a = random.choice(attributes)
    attribute_values = SELECT_COLUMN(examples, a)
    L, M, K = min(attribute_values), max(attribute_values), 1
    while K <= 50:
        threshold = L + K * (M - L) / 51
        gain = INFORMATION_GAIN(examples, a, threshold)
        if gain > max_gain:
            max_gain, best_attribute, best_threshold = gain, a, threshold
        K += 1
    return best_attribute, best_threshold, max_gain

def SELECT_COLUMN(examples, attribute):
    values = []
    for sample in examples:
        values.append(sample[0][attribute])
    return values

def INFORMATION_GAIN(examples, attribute, threshold):
    root_entropy = ENTROPY(frequency(examples))
    K = len(examples)
    leftCount, rightCount = 0, 0
    leftChildren, rightChildren = [0] * (numberOfClasses + 1), [0] * (numberOfClasses + 1)
    for sample in examples:
        # sample[0][n] = value of n-th attribute of the sample
        # sample[1] = the class that sample belongs to
        if sample[0][attribute] < threshold:
            leftCount += 1
            leftChildren[sample[1]] += 1
        else:
             rightCount += 1
             rightChildren[sample[1]] += 1
    left_weight, right_weight = float(leftCount) / float(K), float(rightCount) / float(K)  
    left_entropy, right_entropy = ENTROPY(leftChildren), ENTROPY(rightChildren)
    return root_entropy - left_weight * left_entropy - right_weight * right_entropy

def ENTROPY(numbers):
    numbers.pop() # removed the first item, since there is no item with Class 0
    K = sum(numbers)
    H = 0
    for Ki in numbers:
        ratio = - (Ki / K)
        H += ratio * math.log2(ratio)
    return H

def frequency(examples):
    freq = [0] * (numberOfClasses + 1)
    for sample in examples:
        freq[sample[1]] += 1
    return freq


"""
    ##### The procedure of the program starts here #####
"""


try:
    training_file, test_file, option = sys.argv[1:4]
except:
    print("ERROR : Invalid number of arguments.")
    sys.exit()

# if option != "optimized" and option != "randomized" and option != "forest3" and option != "forest15":
if option not in {"optimized", "randomized", "forest3", "forest15"}:
    print('ERROR : Invalid option.\nOption must be "optimized", "randomized", "forest3" or "forest15".')
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
    print("ERROR : File not found.")
    sys.exit()

# Adding a carraige return at the end of the last line, for convenience
if training_lines[-1] != '\n':
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

"""
print(str(type(examples)))            #  => list       of tuples    
print(str(type(examples[0])))         #  => tuple      of (list_of_float, int)
print(str(type(examples[0][0])))      #  => list       of float
print(str(type(examples[0][0][0])))   #  => float
"""

numberOfClasses = max(examples, key=lambda x: x[1])[1]