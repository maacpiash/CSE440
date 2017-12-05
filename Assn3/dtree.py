import sys, math

class Node:
    # START OF NODE CLASS
    def __init__(self, treeID, nodeID, featID, threshold, infoGain):
        self.treeID = treeID
        self.nodeID = nodeID
        self.featID = featID
        self.threshold = threshold
        self.infoGain = infoGain
        self.left = self.right = None
    
    def printSelfAndChildren(self):
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
    return best_attribute, best_threshold

def SELECT_COLUMN(examples, attribute):
    values = []
    for sample in examples:
        values.append(sample[0][attribute])
    return values

def INFORMATION_GAIN(examples, atribute, threshold):
    return

def ENTROPY(numbers):
    K = sum(numbers)
    H = 0
    for Ki in numbers:
        ratio = Ki / K
        H -= ratio * math.log2(ratio)
    return H    
        

def totalClassesIn(example):
    return
        


        

try:
    training_file, test_file, option = sys.argv[1:4]
except:
    print("INVALID INPUT : Invalid number of CLI arguments")
    sys.exit()

if option != "optimized" and option != "randomized" and option != "forest3" and option != "forest15":
    print('INVALID INPUT : Invalid option.\nOption must be "optimized", "randomized", "forest3" or "forest15"')
    sys.exit()

examples = []

# File I/O
with open(training_file, 'r') as f:
    lines = f.readlines() # took all the lines in a list of strings
if lines[-1] != '\n':
    lines[-1] = lines[-1] + '\n'
    # Added a carraige return at the end of the last line

for oneExample in lines:
    attributes = oneExample.split()
    attrRow = []
    for attr in attributes[:-1]:
        attrRow.append(float(attr))
    cIass = int(oneExample[-2])
    tupl = (attrRow, cIass)
    # Each example data is saved as a tuple in (attribute_array, class) format
    examples.append(tupl)

# print(str(type(examples)))           #  => list    
# print(str(type(examples[0])))        #  => tuple
# print(str(type(examples[0][0])))     #  => list
# print(str(type(examples[0][0][0])))  #  => float