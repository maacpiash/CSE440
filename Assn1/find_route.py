import sys
from collections import deque
from heapq import heappush, heappop

INF = 9999999

class Edge:
# The edges are weighted and undirected.
# This object contains two vertices and the distance between them.
# Vertices v1, v2 are just strings. Distance is a positive integer.
    def __init__(self, v1, v2, distance):
        self.v1 = v1
        self.v2 = v2
        self.distance = int(distance)
        

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
            # Distances between the same pair of nodes in an undirected graph are equal
            self.conns[e.v2][e.v1] = e.distance
        # Distance from one node to the same node = 0
        for v in self.vertices:
            self.conns[v][v] = 0
        # Distance between nodes unreachable to each other = infinity!
        for v1 in self.vertices:
            for v2 in self.vertices:
                if str(self.conns[v1][v2]) == "{}":
                    self.conns[v1][v2] = INF
    
    # *** *** *** Breadth-First Search *** *** *** #
    def BFS(self, startNode):
        # Input validation
        if startNode not in self.vertices:
            print("Invalid input : Vertex is not on graph")
            return
        
        # Data structures initiation
        marked = {}
        for v in self.vertices:
            marked[v] = False
        marked[startNode] = True
        q = deque()
        q.append(startNode)
        print("Breadth-First Search from {startNode}")

        # Main process
        while len(q) > 0:
            v = q.popleft()
            print(v)
            for u in self.vertices:
                if self.conns[u][v] != INF and not marked[u]:
                    q.append(u)
                    marked[u] = True
        return

    # *** *** *** Depth-First Search *** *** *** #
    def DFS(self, startNode, endNode):
        # Input validation
        if startNode not in self.vertices:
            print("Invalid input : Initial vertex is not on graph")
            return
        if endNode not in self.vertices:
            print("Invalid input : Final vertex is not on graph")
            return
        
        # The case of same nodes
        if(startNode == endNode):
            print("Same starting and ending vertices")
            return True
        
        # For nodes sharing an edge, that edge is the shortest path
        dis = self.conns[startNode][endNode]
        if dis != INF:
            print("distance: " + str(dis) + " km")
            print("route:\n" + startNode + " to " + endNode + ": " + str(dis) + "  km")
            return

        # Data structures initiation
        s = list()
        marked = dict()
        backtrack = dict()
        for v in self.vertices:
            marked[v] = False
        s.append(startNode)
        marked[startNode] = True
        found = False

        # Main process
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
        
        # Backtracking and printing results
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
    
    # *** *** *** Dijkstra's Algorithm *** *** *** #
    def Dijkstra(self, node1, node2):
        # Inputs validation
        if node1 not in self.vertices:
            print("Invalid input : Initial vertex is not on graph")
            return
        if node2 not in self.vertices:
            print("Invalid input : Final vertex is not on graph")
            return
        
        # The case of same nodes
        if(node1 == node2):
            print("Same starting and ending vertices")
            return True
        
        # For nodes sharing an edge, that edge is the shortest path
        dis = self.conns[node1][node2]
        if dis != INF:
            print("distance: " + str(dis) + " km")
            print("route:\n" + node1 + " to " + node2 + ": " + str(dis) + "  km")
            return
        
        # Data structures initiation
        visited = dict()
        for nodes in self.vertices:
            visited[nodes] = None
        prioQ = [(0, node1, None)]
        tracer = [(0, node1, None)]
        
        # Main process
        while len(prioQ) > 0:
            tempLen, tempNode, tempPre = heappop(prioQ)
            tracer.append((tempLen, tempNode, tempPre))
            if(visited[tempNode] == None):
                visited[tempNode] = tempLen
                for v in self.vertices:
                    newLen = self.conns[v][tempNode]
                    if newLen != INF and visited[v] == None:
                        heappush(prioQ, (tempLen + newLen, v, tempNode))
        
        # Handling unreachable nodes           
        if str(visited[node2]) == "None":
            print("distance: infinity\nroute:\nnone")
            return
        
        # Backtracking and printing results
        stack = []
        node = node2
        path = 0
        while node != node1:
            for i in tracer:
                if i[1] == node:
                    newNode = i[2]
                    break
            length = self.conns[node][newNode]
            stack.append(str(newNode + " to " + node + ", " + str(length) + " km"))
            path = path + length
            node = newNode
        print("distance: " + str(path) + " km")
        for items in reversed(stack):
            print(items)


"""
    ##### The procedure of the program starts here #####
"""

try:
    inputf = sys.argv[1]
    node1 = sys.argv[2]
    node2 = sys.argv[3]
except:
    print("INVALID INPUT")
    sys.exit()

# File I/O
with open(inputf, 'r') as f:
    lines = f.readlines()

routes = []
# This list of STRINGS will contain all the members of 'lines' upto (and excluding) "END OF INPUT"

for r in lines:
    if "END OF INPUT" in r:
        break
    else:
        routes.append(r)

graph = Graph(routes)

graph.Dijkstra(node1, node2)