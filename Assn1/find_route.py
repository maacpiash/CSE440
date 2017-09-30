import sys
from collections import deque

INF = 9999999

class Edge:
# The edges are weighted and undirected.
# This object contains two vertices and the distance between them.
# Vertices v1, v2 are just strings. Distance is a positive integer.
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
# The edges of this Graph are weighted and undirected.
# This object contains a list of eList and a list of vList.
# Edges are Edge objects. Vertices are strings.
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
            self.conns[e.v2][e.v1] = e.distance
        # Distance between same nodes = 0
        for v in self.vertices:
            self.conns[v][v] = 0
        # Distance between unreachable nodes = infinity!
        for v1 in self.vertices:
            for v2 in self.vertices:
                if str(self.conns[v1][v2]) == "{}":
                    self.conns[v1][v2] = INF
    
    # *** *** *** Breadth-First Search *** *** ***
    def BFS(self, startNode):
        marked = {}
        for v in self.vertices:
            marked[v] = False
        marked[startNode] = True
        q = deque()
        q.append(startNode)
        print("Breadth-First Search from " + str(startNode))
        while len(q) > 0:
            v = q.popleft()
            print(v)
            for u in self.vertices:
                if self.conns[u][v] != INF and not marked[u]:
                    q.append(u)
                    marked[u] = True
        return

    # *** *** *** Depth-First Search *** *** ***
    def DFS(self, startNode, endNode):
        s = list()
        marked = dict()
        backtrack = dict()
        for v in self.vertices:
            marked[v] = False
        s.append(startNode)
        marked[startNode] = True
        found = False
        if(startNode == endNode):
            print("Same starting and ending vertices")
            return True
        # print("Depth-First Search from "+ startNode + " to " + endNode + ":")
        while len(s) > 0:
            k = s.pop()
            if(k == endNode):
                found = True
                break
            for i in reversed(self.vertices):
                if self.conns[k][i] != INF and not marked[i]:
                    s.append(i)
                    backtrack.update({i : k})
                    marked[i] = True
        if(found):
            stack = []
            routelength = 0
            node = endNode
            while node != startNode:
                newNode = backtrack[node]
                length = self.conns[node][newNode]
                stack.append(str(newNode + " to " + node + ", " + str(length) + " km"))
                routelength += length
                node = newNode
            print("distance: " + str(routelength) + " km")
            for items in reversed(stack):
                print(items)
        else:
            print("distance: infinity\nroute:\nnone")
        return found


"""
    ##### The procedure of the program starts here #####
"""

inputf = sys.argv[1]
node1 = sys.argv[2]
node2 = sys.argv[3]

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

graph.DFS(node1, node2)

