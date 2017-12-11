import os

li1 = ["satellite_training.txt", "pendigits_training.txt", "yeast_training.txt"]
li2 = ["satellite_test.txt", "pendigits_test.txt", "yeast_test.txt"]
li0 = ["Satellite", "Pendigits", "Yeast"]

for f in range(3):
    print("Dataset: " + li0[f])
    for K in range(1, 20, 2):
        os.system("python classify.py " + li1[f] + " " + li2[f] + " knn " + str(K))
