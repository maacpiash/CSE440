import sys, math, random

pruning_thr = 50
global_classes_count = 0
global_attribs_count = 0
global_option = None
global_classes_list = []
global_forest = []
global_trees_count = 0
global_parent_nodeID = 0

""" 'Sample' class definition """

class Sample:
    def __init__(self, attributes, Class):
        self.attributes = attributes
        self.Class = Class

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

""" 'Node' class definition """

class Node:
    # START OF NODE CLASS
    def __init__(self, treeID, nodeID, featID, threshold, infoGain):
        self.treeID = treeID
        self.nodeID = nodeID
        self.featID = featID
        self.threshold = threshold
        self.infoGain = infoGain
        self.left_child = self.right_child = None

    def getValue(self, sample):
        if sample.attributes[self.featID] < self.threshold:
            if type(self.left_child) is Node:
                return self.left_child.getValue(sample)
            else:
                return self.left_child
        else:
            if type(self.right_child) is Node:
                return self.right_child.getValue(sample)
            else:
                return self.right_child

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

""" Tree printing and File I/O functions' definition """
    
def Console_WriteLine(tree):
    # An homage to C#
    q = []
    q.append(tree)
    while len(q) > 0: 
        node = q.pop(0)       
        print("tree=%2d, node=%3d, feature=%2d, thr=%6.2lf, gain=%lf" % (tree.treeID, node.nodeID, node.featID, node.threshold, node.infoGain))
        global_parent_nodeID = node.nodeID
        if type(node.left_child) is Node:
            q.append(node.left_child)
        else:
            print("tree=%2d, node=%3d, feature=-1, thr=-1, gain=-1" % (tree.treeID, global_parent_nodeID * 2))
        if type(node.right_child) is Node:
            q.append(node.right_child)
        else:
           print("tree=%2d, node=%3d, feature=-1, thr=-1, gain=-1" % (tree.treeID, global_parent_nodeID * 2 + 1))
            
def getSamplesFromFile(inputFile):
    try:
        with open(inputFile, 'r') as f:
            lines = f.readlines() # took all the lines in a list of strings
    except:
        print("ERROR : File could not be opened.")
        sys.exit()
    sampleList = []
    if lines[-1] != '\n':
        # Adding a carraige return at the end of the last line, for convenience
        lines[-1] = lines[-1] + '\n'
    for oneExample in lines:
        attributes = oneExample.split()
        attrRow = []
        for attr in attributes[:-1]:
            attrRow.append(float(attr))
        try:
            cIass = int(oneExample[-2])
        except:
            cIass = int(oneExample[-3])
        sampleList.append(Sample(attrRow, cIass))
    return sampleList


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

""" DTL functions' definition """

def DTL(examples, default, treeID, nodeID): # OK
    if len(examples) < pruning_thr:
        return default
    elif homogeneous(examples):
        return examples[0].Class
    else:
        if global_option == "optimized":
            best_attribute, best_threshold, max_gain = CHOOSE_ATTRIBUTE(examples)
        else:
            best_attribute, best_threshold, max_gain = RANDOM_ATTRIBUTE(examples)
        tree = Node(treeID, nodeID, best_attribute, best_threshold, max_gain)
        examples_left, examples_right = seperate(examples, best_attribute, best_threshold)
        tree.left_child = DTL(examples_left, DISTRIBUTION(examples), treeID, nodeID * 2)
        tree.right_child = DTL(examples_right, DISTRIBUTION(examples), treeID, nodeID * 2 + 1)
        return tree

def CHOOSE_ATTRIBUTE(examples): # OK
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

def RANDOM_ATTRIBUTE(examples): # OK
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

""" Helper functions' definition """

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
examples = getSamplesFromFile(training_file)
testers = getSamplesFromFile(test_file)

for sample in examples:
    c = sample.Class
    if c not in global_classes_list:
            global_classes_list.append(c)

global_attribs_count = len(examples[0].attributes)
global_classes_count = len(global_classes_list)

if global_option in {"optimized", "randomized"}:
    global_trees_count = 1
else:
    global_trees_count = 3 if global_option == "forest3" else 15

# print(global_classes_list)

for i in range(global_trees_count):
    decision_tree = DTL(examples, DISTRIBUTION(examples), i, 1)
    global_forest.append(decision_tree)
    Console_WriteLine(decision_tree)

accuracy_list = []
ac_pc = []
n = len(global_forest)
object_id = 0
total = 0

for tree in global_forest:
    print("\nClassification : Tree " + str(tree.treeID))
    accuracy = 0
    for sample in testers:
        vector = tree.getValue(sample)
        try:
            m = max(vector)
            prediction = vector.index(m)
            count = 0
            for value in vector:
                if value == m:
                    count += 1
            accuracy = 1 / count
        except:
            prediction = vector
            # in case of homogeneous examples, DTL returns integer
            accuracy = 1
        if int(prediction) != int(sample.Class):
            accuracy = 0
        print("ID=%5d, predicted=%3d, true=%3d, accuracy=%4.2lf" % (object_id, prediction, sample.Class, accuracy))
        object_id += 1
        accuracy_list.append(accuracy)
    pc = sum(accuracy_list) * 100.0 / len(accuracy_list)
    ac_pc.append(pc)
print()
for i in range(n):
    print("Rate of success for Tree %2d : %3.2lf per cent" % (i, ac_pc[i]))
total = sum(ac_pc)
avg = total / n

print("\nOverall rate of success for %d tree(s): %6.2lf per cent" % (n, avg))