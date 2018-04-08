## Assignment 3
Submitted on December 9, 2017<br>
 
### Problem: Decision Tree Learning
The task here is to implement decision tree learning algorithm for machine learning. First, the program *learns* from given data in the training file and builds a decision tree based on *best attribute*, *maximum gain* and *best threshold*. Then the program tries to predict the *classes* of the data from the *test file*. The accuracy of prediction is given as the output.

#### Input format:
```
$ python dtree.py [training_file] [test_file] [option]
```
For example: `$ python dtree.py yeast_training.txt yeast_test.txt forest3`<br/>
There are 4 options to choose from:
- `optimized` generates a decision tree based on the *best attribute* and the *best threshold* at every level.
- `randomized` generates a decision tree based on an *attribute* chosen randomly. However, the *threshold* is not randomly set.
- `forest3` generates a decision forest of three randomized decision trees and gives the average output.
- `forest15` generates a decision forest of fifteen randomized decision trees and gives the average output.

**Note:** The *pruning threshold* is set to 50, inside the source code