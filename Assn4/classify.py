import sys, math, statistics

global_learning_examples = None
global_testing_examples = None
global_atrrib_count = 0

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
    alldata = []
    for i in range(global_atrrib_count):
        alldata.append(list())
    new_examples = []
    for sample in examples:
        new_examples.append(Sample([0 for i in range(global_atrrib_count)], sample.Class))
    mean = []
    stddev = []
    for sample in examples:
        for i in range(global_atrrib_count):
            alldata[i].append(sample.attributes[i])
    for column in alldata:
        stddev.append(statistics.stdev(column))
        mean.append(statistics.mean(column))
    for i in range(len(examples)):
        for j in range(global_atrrib_count):
            new_examples[i].attributes[j] = (sample.attributes[j] - mean[j]) / stddev[j]
    return new_examples

def L2(test, train):
    prediction = train.Class
    distance = 0.0
    for i in range(global_atrrib_count):
        distance += math.pow((test.attributes[i] - train.attributes[i]), 2)
    distance = math.sqrt(distance)
    return (distance, prediction)

try:
    training_file, test_file = sys.argv[1:3]
    global_k = int(sys.argv[4])
except:
    print("ERROR : Invalid number of arguments.")
    sys.exit()

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
    try:
        predicted_class = statistics.mode(predictions)
    except:
        # mode function throws exception if each element in the list occurs exactly once
        predicted_class = predictions[0]
    true_class = test_sample.Class
    if(test_sample.Class != predicted_class):
        accuracy = 0
        failure += 1
    else:
        accuracy = 1 / predictions.count(predicted_class)
        success += 1
    print("ID=%5d, predicted=%3d, true=%3d, accuracy=%4.2lf" % (object_id, predicted_class, true_class, accuracy))
    score.append(accuracy)
    object_id += 1

print("Occurences of success: " + str(success))
print("Occurences of failure: " + str(failure))
print("Average accuracy = %4.2lf per cent." % (statistics.mean(score) * 100))