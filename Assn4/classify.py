import sys

global_learning_examples = []
global_testing_examples = []
global_distances = []

""" Sample class definition """

class Sample:
    def __init__(self, attributes, Class):
        self.attributes = attributes
        self.Class = Class

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

def Normalize(examples):
    return
    

try:
    training_file, test_file, classifier_type, global_k = sys.argv[1:5]
except:
    print("ERROR : Invalid number of arguments.")
    sys.exit()

learning_examples = getSamplesFromFile(training_file)
testing_examples = getSamplesFromFile(test_file)

