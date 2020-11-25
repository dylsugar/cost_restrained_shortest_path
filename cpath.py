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

    def inHeap(self,heap,vertex):
        for x in heap:
            if x[1] == vertex:
                return True
        return False
    
    def getCostime(self,heap,vertex):
        for x in heap:
            if x[1] == vertex:
                return x[2],x[3]

    def poppedHeap(self,heap,vertex):
        c = 0
        for x in heap:
            if x[1] == vertex:
                heap.pop(c)
            c+=1
        return heap

    def dupCheck(self, P):
        return [x for x in (set(tuple(i) for i in P))]
    
    def pathFinder(self,path,dest,start,l):
        c = 0 
        l.append(dest)
        while dest != start:
            tmp = []
            count = 0
            for x in path:
                if x[3] == dest:
                    count +=1
                    tmp.append((x[0],x[1],x[2]))
            
            c = "INF"
            t = 0
            v = 0
            for y in tmp:
                if c == "INF":
                    c = y[0]
                    t = y[1]
                    v = y[2]
                elif c > y[0]:
                    c = y[0]
                    t = y[1]
                    v = y[2]
                elif c == y[0]:
                    if (int(start) - int(v)) < (int(start) - int(y[2])):
                        v = y[2]
                        c = y[0]
                        t = y[1]
            l.append(v)
            dest = v
        return l
         
    def trip_algorithm(self, Source, Dest, Budget):
        heap = []
        start = Source
        find_source = dict()
        visited = []
        P = []
        path = []
        c = 0
        cost = 0
        time = 0
        heap.append((Source,Source,cost,time))
        print("------------------------------------------")
        while heap:
            P.append((cost,time,Source))
            heap = self.poppedHeap(heap,Source)
            out_edges = []
            count = 0
            
            for e in self.edges[Source]: 
                if e not in visited and self.inHeap(heap,e):
                    c_cost, c_time = self.getCostime(heap,e)
                    P.append((c_cost, c_time, e))
                    path.append((c_cost,c_time,Source,e))
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
                    min_source = y[0]
                    min_vertex = y[1]
                    min_cost = y[2]
                    min_time = y[3]
                elif min_cost > y[2]:
                    min_source = y[0]
                    min_vertex = y[1]
                    min_cost = y[2]
                    min_time = y[3]
                elif min_cost == y[2]:
                    if min_time > y[3]:
                        min_source = y[0]
                        min_time = y[3]
                        min_vertex = y[1]
            path.append((min_cost,min_time,min_source,min_vertex))
            time = min_time
            cost = min_cost
            Source = min_vertex
            visited.append(Source)
        P = self.dupCheck(P)
        print("FORMAT : (Cost, Time, Vertex)\n")
        print("Increasing Cost: ")
        costlist = sorted(P, key = lambda x: x[0])
        timelist = sorted(P, key = lambda x: x[1])
        for i in costlist:
            print(i)
        print("\nDecreasing Time: ")
        for j in reversed(timelist):
            print(j)
        print("-----------Part Two Below-----------------")
        dapath = self.pathFinder(path,Dest,start,list())
        u = 0
        for x in P:
            if x[2] == Dest:
                print("Cost: " + str(x[0]) + " Traversal Time: " + str(x[1]))

        for d in reversed(dapath):
            print(" --> " + str(d),end='')
        print("\n")




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
    print("------------Part One Below-----------------")
    edge_list = []
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
    
    g.trip_algorithm(source,destination,budget)


if __name__ == "__main__":
    main(sys.argv[1:])
