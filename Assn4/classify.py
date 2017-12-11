import sys, math, statistics

global_learning_examples = None
global_testing_examples = None
global_atrrib_count = 0

class Sample:
    def __init__(self, attributes, Class):
        self.attributes = attributes
        self.Class = Class

def getSamplesFromFile(inputFile):
    # reads data from file and returns a list of Sample objects
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
        attributes = oneExample.split() # seperated by space
        attrRow = []
        for attr in attributes[:-1]:
            attrRow.append(float(attr))
        try:
            cIass = int(oneExample[-2])
        except: # handling newline character at the end of the line
            cIass = int(oneExample[-3])
        sampleList.append(Sample(attrRow, cIass))
    return sampleList

def Normalize(examples):
    # normalizes dataset by mean and standard deviation of each attribute
    alldata = []
    for i in range(global_atrrib_count):
        alldata.append(list())
    # list of all attributes' values. 2-dimensional list
    new_examples = []
    # this list will hold the adjusted data points
    for sample in examples:
        new_examples.append(Sample([0 for i in range(global_atrrib_count)], sample.Class))
    # initialized with zeroes
    mean = []
    stddev = []
    # list of mean and standard deviations of all attributes
    for sample in examples:
        for i in range(global_atrrib_count):
            alldata[i].append(sample.attributes[i])
    # i-th attribute value of each data point is appended to the i-th list of alldata
    for column in alldata:
        stddev.append(statistics.stdev(column))
        mean.append(statistics.mean(column))
    # mean and standard deviation for each attribute is appended to the lists
    for i in range(len(examples)):
        for j in range(global_atrrib_count):
            new_examples[i].attributes[j] = (examples[i].attributes[j] - mean[j]) / stddev[j]
    # data points from examples list are adjusted and appended into new_examples list
    return new_examples

def L2(test, train):
    # calculates Eucledian distance between data points
    # returns both the distance and the class of training data point
    prediction = train.Class
    distance = 0.0
    for i in range(global_atrrib_count):
        distance += math.pow((test.attributes[i] - train.attributes[i]), 2)
    distance = math.sqrt(distance)
    return (distance, prediction)

def Accuracy(prediction):
    # takes the array of K class numbers and returns the accuracy value. for tied classes,
    # the function returns a list of possible classes and how many times each class occurs.
    try:
        return statistics.mode(prediction)
    except:
        frequency = dict.fromkeys(prediction)
        keys = frequency.keys()
        classes = []
        for k in keys:
            frequency[k] = 0
        for classnum in prediction:
            frequency[classnum] += 1
        occurence = max(frequency.values())
        for k in keys:
            if frequency[k] == occurence:
                classes.append(k)
        return (classes, occurence)

""" Program process """

try:
    training_file, test_file = sys.argv[1:3]
    global_k = int(sys.argv[4])
except:
    print("ERROR : Invalid number of arguments.")
    sys.exit()

"""
value = Accuracy([2, 4, 2, 4, 4, 2])
if type(value) == int:
    print(str(value))
else:
    print(value[0])
    print(value[1])
"""

learning_examples = getSamplesFromFile(training_file)
testing_examples = getSamplesFromFile(test_file)

global_atrrib_count = len(learning_examples[0].attributes)

global_learning_examples = Normalize(learning_examples)
global_testing_examples = Normalize(testing_examples)

score = []
object_id = 0
success, failure = 0, 0

for test_sample in global_testing_examples:
    distances = []
    predictions = []
    for training_sample in global_learning_examples:
        distances.append(L2(test_sample, training_sample))
    distances.sort(key=lambda tupl: tupl[0])
    # predictions.append(item[1] for item in distances[:global_k])
    for i in range(global_k):
        predictions.append(distances[i][1])
    value = Accuracy(predictions)
    true_class = test_sample.Class

    if type(value) == int:
        predicted_class = value
        if(test_sample.Class != value):
            accuracy = 0
        else:
            accuracy = 1
    else:
        if predicted_class in value[0]:
            accuracy = 1 / value[1]
        else:
            accuracy = 0
    if accuracy == 0:
        failure += 1
    else:
        success += 1
    print("ID=%5d, predicted=%3d, true=%3d, accuracy=%4.2lf" % (object_id, predicted_class, true_class, accuracy))
    score.append(accuracy)
    object_id += 1

# print("K = %2d : Accuracy = %3.2lf%%" % (global_k, statistics.mean(score) * 100))


print("+-------------------------------------------------------+")
print("| Result after considering %2d Nearest Neighbors:\t|" % (global_k))
print("| Total number of objects: " + str(success + failure) + "\t\t\t\t|")
print("| Occurences of success (considering tie = 1.0): " + str(success) + "\t|")
print("| Occurences of failure: " + str(failure) + "\t\t\t\t|")
print("| Average accuracy (assuming tie = 1.0) = %4.2lf %%" % (success / (success + failure) * 100) + "\t|")
print("| Average accuracy (calculating for ties) = %4.2lf %%" % (statistics.mean(score) * 100) + "\t|")
print("+-------------------------------------------------------+")
