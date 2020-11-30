#!/usr/bin/python

import sys, getopt
from collections import defaultdict

class Graph():
    def __init__(self):
        self.edges = defaultdict(list)  
        self.vertices = []
        self.cost = {}
        self.time = {}

    def addVertex(self,value):
        self.vertices.append(value)

    
    def addEdge(self, start_v, end_v, cost, time):
        self.edges[start_v].append(end_v)
        self.cost[(start_v,end_v)] = cost
        self.time[(start_v,end_v)] = time

    def poppedHeap(self,heap,vertex):
        """
        Pops the vertex from the list/heap and returns the heap.
        """
        c = 0
        for x in heap:
            if x == vertex:
                heap.pop(c)
                break
            c+=1
        return heap

    def pathFinder(self,path,dest,start,l):
        """
        The shortest path is returned by only looking at the smallest cost and setting destination
        to that cost.
        """
        shortest_path = []
        end = True
        shortest_path.append(dest)
        while end == True:
            min_cost = "INF"
            min_time = "INF"
            min_in = "INF"
            for x in path:
                if dest == x[3]:
                    if min_cost == "INF":
                        min_cost = x[0]
                        min_time = x[1]
                        min_in = x[2]
                    elif min_cost > x[0]:
                        min_cost = x[0]
                        min_time = x[1]
                        min_in = x[2]
            dest = min_in
            if min_in == start:
                end = False
            shortest_path.append(min_in)
        return shortest_path


    def minValue(self, heap):
        """
        Finds minimum cost value in both heap any list. Vertex is returned
        """
        min_cost = "INF"
        min_time = 0
        min_out = 0
        for h in heap:
            if h:
                if min_cost == "INF":
                    min_cost = h[0]
                    min_time = h[1]
                    min_out = h[2]
                elif min_cost > h[0]:
                    min_cost = h[0]
                    min_time = h[1]
                    min_out = h[2]
                elif min_cost == h[0]:
                    if min_time > h[1]:
                        min_cost = h[0]
                        min_time = h[1]
                        min_out = h[2]
        return (min_cost, min_time, min_out)

    
    def minTime(self, heap):
        """
        Finds minimum time value in the heap and returns that vertex
        """
        min_cost = 0
        min_time = "INF"
        min_out = 0
        for h in heap:
            if h:
                if min_time == "INF":
                    min_cost = h[0]
                    min_time = h[1]
                    min_out = h[2]
                elif min_time > h[1]:
                    min_cost = h[0]
                    min_time = h[1]
                    min_out = h[2]
        return min_time


    def cost_option_algorithm(self, Src, Dest, Budget):
        """
        Primary Algorithm that finds shortest paths based on Trade off curves
        """

        #Trade off curves of options
        P = [[] for Null in range(len(self.vertices))]

        #next adjacent paths for current vertex
        Adj = [[] for Null in range(len(self.vertices))]

        #holds previous vertex
        Path = []

        #acts like a priority queue
        heap = []
        cost = 0
        time = 0
        Source = ((cost, time, Src))
        heap.append(Source) # weight is cost basically
        Path.append((cost, time, Src, Src))
        while heap:
            # Source[0] is the cost weight of the vertex
            # Source[1] is the time weight of the vertex
            # Source[2] is the vertex label

            # poppedHeap finds Source which is has the minimum cost and pops it
            heap = self.poppedHeap(heap,Source)
            
            #find vertex min in trade off curves
            m = self.minValue(P[int(Source[2])])
            cost = m[int(0)]
            time = self.minTime(P[int(Source[2])])
            
            # there is no other min value
            if len(P[int(Source[2])]) == 0 or Source[0] < cost or Source[1] < time:
                P[int(Source[2])].append(Source)
            out_edges = []

            # neighbor vertices from current
            for e in self.edges[Source[2]]:
                out_edges.append(e)
            
            # checks if addition of x neigbor vertice will disrupt curve
            for x in out_edges:
                m_tmp = self.minValue(P[int(x)])
                cost = m_tmp[0]
                time = self.minTime(P[int(x)])
                total_cost = int(Source[0]) + int(self.cost[Source[2], x])
                total_time = int(Source[1]) + int(self.time[Source[2], x])
                if len(P[int(x)]) == 0 or total_cost < cost or total_time < time:
                    # makes sure vertices we can reach are used
                    if int(total_cost) <= int(Budget):
                        adj_insert = (total_cost - int(Source[0]), total_time - int(Source[1]), x)
                        if adj_insert not in Adj[int(Source[2])]:
                            Adj[int(Source[2])].append((adj_insert))
                        heap.append((total_cost, total_time, x))
                        Path.append((total_cost, total_time, Source[2], x))        
            
            Source = self.minValue(heap)
        return P,Path,Adj 
        
def main(argv):
    
    f = open(argv[0],"r")
    source = argv[1]
    destination = argv[2]
    budget = argv[3]
    print("-------------  Read File  ------------------")
    print("File Name: " +argv[0])
    print("Source Vertex: " + source)
    print("Destination Vertex: " + destination)
    print("Budget: " + budget)
    print("\n------------- Read Contents -----------------")
    edge_list = []
    vertices = set()
    while True:

        line = f.readline()
        tmp = []
        ec = 0
        newline = line.split()
        edge_list.append(tuple(newline))

        if not line:
            break
    edge_list.pop(len(edge_list)-1)
    g = Graph()
    for y in edge_list:
        print(y[0] + " -- to --> " + y[1] + " with Cost: "+y[2] + " and Time: " + y[3])
        g.addEdge(y[0],y[1],y[2],y[3])
        vertices.add(y[0])
        vertices.add(y[1])
    for l in list(vertices):
        g.addVertex(l)
    print("\n---------Part 1: Adjacency List-------------")
    print("FORMAT: (Cost, Time, Vertex)\n\n")
    p, path, adj = g.cost_option_algorithm(source,destination,budget)
    count = 0
    for a in adj:
        print("P[" + str(count) + "] --> "+ str(a))
        count+=1
    count = 0
    shortest = 0
    print("\n-------- Part 1: Shortest Paths ------------")
    print("FORMAT: (Cost, Time, Vertex)\n\n")
    for i in p:
        print("P[" + str(count) + "] --> "+ str(i))
        if count == int(destination):
            shortest = i[0]
        count+=1
    shortest_path = g.pathFinder(path,destination,source,list())
    print("\n------------ Part 2: Final Path -------------")
    if shortest_path:
        print("Vertex - to - Vertex Path: ")
        for r in reversed(shortest_path):
            print(" -> " + str(r),end='')
        print("\n")
        print("Traversal of Shortest Path from " + str(source) + " to " + str(destination) + ": ")
        if shortest:
            print("Cost = " + str(shortest[0]))
            print("Time = " + str(shortest[1]))
    else:
        print("There is no Path reported!")
    print("\n---------------------------------------------")
    print("\n\n\n")


if __name__ == "__main__":
    main(sys.argv[1:])
