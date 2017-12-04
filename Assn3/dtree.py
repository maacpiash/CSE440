import sys

# Node class will be here, hopefully by today!

"""
    ##### The procedure of the program starts here #####
"""

try:
    training_file, test_file, option = sys.argv
except:
    print("INVALID INPUT")
    sys.exit()

if option != "optimized" and option != "randomized" and option != "forest3" and option != "forest15":
    print("INVALID INPUT")
    sys.exit()

examples = []

# File I/O
with open(training_file, 'r') as f:
    lines = f.readlines() # took all the lines in a list of strings

for oneExample in lines:
    attributes = oneExample.split()
    attrRow = []
    for attr in attributes[:-1]:
        attrRow.append(float(attr))
    claas = int(oneExample[-1])
    tupl = (attrRow, claas) # Each example data is saved as a tuple (array of attributes, class)
    examples.append(tupl)
