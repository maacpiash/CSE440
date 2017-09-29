import sys

class Edge:
# The eList are weighted and undirected.
# This object contains two vList and the distance between them.
# vList v1, v2 are just strings. Distance is a positive integer.
    def __init__(self, v1, v2, distance):
        self.v1 = v1
        self.v2 = v2
        self.distance = int(distance)

    def printEdge(self):
        print(self.v1 + " to " + self.v2 + ", " + str(self.distance) + " km")

class Connections(dict):
# Found this code on Wikipedia (https://en.wikipedia.org/wiki/Autovivification)
# Basically a child class of dict class, an implementation of dynamic 2D dictionary
# Dictionary structure => Connections[Vertex1][Vertex2] = distance
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

class Graph:
# The eList of this Graph are weighted and undirected.
# This object contains a list of eList and a list of vList.
# eList are Edge objects. vList are strings.
    def __init__(self, routes):
        eList = []
        vList = []
        for r in routes:
            a, b, c = r.split(' ')
            eList.append(Edge(a, b, c))
            if(vList.__contains__(a) == False):
                vList.append(a)
            if(vList.__contains__(b) == False):
                vList.append(b)
        self.edges = eList
        self.vertices = vList
        self.conns = Connections()
        for e in self.edges:
            self.conns[e.v1][e.v2] = e.distance


""" The procedure of the program starts here """

inputf = sys.argv[1]

# File I/O
with open(inputf, 'r') as f:
    lines = f.readlines()

routes = []
# This list of STRINGS will contain all the members of 'lines' upto (and excluding) "END OF INPUT"

for r in lines:
    if(r == str("END OF INPUT")):
        break
    else:
        routes.append(r)

graph = Graph(routes)