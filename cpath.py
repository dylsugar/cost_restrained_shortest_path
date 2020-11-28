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


    def cost_option_algorithm(self, Source, Dest, Budget):
        start = Source
        P = [] # each vertice with trade off curve
        vertex_cost_find = dict()
        heap = []
        neighbors = set()
        cost = 0
        time = 0
        c = 0
        heap.append((Source, Source, cost, time))
        P.append((cost, time, Source,Source))
        print("------------PART ONE BELOW----------------")
        while heap:
            self.addVertex(Source)
            heap = self.poppedHeap(heap,Source)
            out_edges = []
            future_list = []
            for e in self.edges[Source]:
                out_edges.append(e)
            for o in out_edges:
                tmp_cost = int(self.cost[(Source,o)]) + cost
                t = int(self.cost[(Source,o)])
                tmp_time = int(self.time[(Source,o)]) + time
                c = int(self.time[(Source,o)])
                fp = True
                cp = True
                if Source != start:
                    if len(out_edges) > 2:
                        for x in out_edges:
                            if o != x:
                                if o in self.edges[x]:
                                    fp = True
                                    break
                                else:
                                   fp = False
                if fp == True:
                    heap.append((Source, o, tmp_cost, tmp_time))
                P.append((tmp_cost,tmp_time, Source, o))
            min_neighbor = 0
            min_cost = "INF"
            min_time = 0
            for h in heap:
                if min_cost == "INF":
                    min_neighbor = h[1]
                    min_cost = h[2]
                    min_time = h[3]
                elif min_cost > h[2]:
                    min_neighbor = h[1]
                    min_cost = h[2]
                    min_time = h[3]
                elif min_cost == h[2]:
                    if min_time > h[3]:
                        min_neighbor = h[1]
                        min_cost = h[2]
                        min_time = h[3]
            
            Source = min_neighbor
            cost = min_cost
            time = min_time
        print("Adjacency: ")
        for i in range(len(self.vertices)+1):
            print("P["+ str(i) +"] = ", end = "")
            for y in P:
                if int(y[3]) == int(i):
                    print("<("+str(y[0])+","+str(y[1])+"),"+str(y[2]), end = "")
            print("\n")
        print("Shortest Path sth like: ")
        for i in range(len(self.vertices)+1):
           print("P["+ str(i) +"] = ", end = "")
           for x in P:
               if int(x[3]) == int(i):
                print("<("+str(x[0])+","+str(x[1])+"),"+str(x[3])+" >  ", end = "")
           print("\n")
        print("----------------PART TWO BELOW----------------------")
        for x in P:
            if x[3] == Dest:
                print("Cost: " + str(x[0]) + " Traversal Time: " + str(x[1]))
        dapath = self.pathFinder(P,Dest,start,list())
        for d in reversed(dapath):
            print(" --> " + str(d),end='')
        print("\n")




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
        print("HEAP : From To Cost Time ")
        while heap:
            print(Source)
            #print(heap)
            P.append((cost,time,Source))
            heap = self.poppedHeap(heap,Source)
            out_edges = []
            count = 0
            for e in self.edges[Source]: 
                #if self.inHeap(heap,e):
                #    c_cost, c_time = self.getCostime(heap,e)
                #    P.append((c_cost, c_time, e))
                #    path.append((c_cost,c_time,Source,e))
                #else:
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
            if c == 20:
                break
            c += 1
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
    
    g.cost_option_algorithm(source,destination,budget)


if __name__ == "__main__":
    main(sys.argv[1:])
