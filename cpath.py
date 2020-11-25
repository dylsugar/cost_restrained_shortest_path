#!/usr/bin/python

import sys, getopt
from collections import defaultdict
import networkx

class Graph():
    def __init__(self):
        self.edges = defaultdict(list)  
        self.vertices = set()
        self.cost = {}
        self.time = {}

    def addVertex(self,value):
        self.vertices.add(value)

    
    def addEdge(self, start_v, end_v, cost, time):
        self.edges[start_v].append(end_v)
        self.cost[(start_v,end_v)] = cost
        self.time[(start_v,end_v)] = time

    
    def trip_algorithm(self, Source, Dest, Budget):
        heap = []
        visited = []
        P = []
        c = 0
        cost = 0
        time = 0
        heap.append((Source,Source,cost,time))
        print("------------------------------------------")
        while heap:
            P.append((cost,time,Source))
            count = 0
            for x in heap:
                if x[1] == Source:
                    heap.pop(count)
                count+=1
            out_edges = []
            count = 0
            for e in self.edges[Source]: 
                if e not in visited:
                    out_edges.append((Source, e))
            
            # Heap ( From , To, Cost, Time ) format
            for x in out_edges:
                this_cost = int(self.cost[(x[0],x[1])]) + cost
                this_time = int(self.time[(x[0],x[1])]) + time
                heap.append((x[0],x[1],this_cost, this_time))
            
            min_source = 0
            min_vertex = 0
            min_cost = "INF"
            min_time = 0
            for y in heap:
                if min_cost == "INF":
                    min_vertex = y[1]
                    min_cost = y[2]
                    min_time = y[3]
                elif min_cost > y[2]:
                    min_vertex = y[1]
                    min_cost = y[2]
                    min_time = y[3]


            
            time = min_time
            cost = min_cost
            Source = min_vertex
            visited.append(Source)
        
        print("(Cost, Time, Vertex)")
        print("Increasing Cost: ")
        for i in P:
            print(i)
        print("\nDecreasing Time: ")
        for i in reversed(P):
            print(i)
        
        print("\n\n\n")

def main(argv):
    
    f = open(argv[0],"r")
    source = argv[1]
    destination = argv[2]
    budget = argv[3]
    print("------------------------------------------")
    print("File Name: " +argv[0])
    print("Source Vertex: " + source)
    print("Destination Vertex: " + destination)
    print("Budget: " + budget)
    print("-------------------------------------------")
    edge_list = []
    while True:

        line = f.readline()
        tmp = []
        ec = 0
        for x in line:
            if x.isnumeric():
                tmp.append(x)
        
        edge_list.append(tuple(tmp))


        if not line:
            break
    edge_list.pop(len(edge_list)-1)
    g = Graph()
    for y in edge_list:
        print(y[0] + " -- to --> " + y[1] + " with Cost: "+y[2] + " and Time: " + y[3])
        g.addEdge(y[0],y[1],y[2],y[3])
    
    g.trip_algorithm(source,destination,budget)


if __name__ == "__main__":
    main(sys.argv[1:])
