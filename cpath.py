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
            if x == vertex:
                heap.pop(c)
                break
            c+=1
        return heap

    def dupCheck(self, P):
        return [x for x in (set(tuple(i) for i in P))]
    
    def pathFinder(self,path,dest,start,l):
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
        
        P = [[] for Null in range(7)]
        Adj = [[] for Null in range(7)]
        Path = []
        heap = []
        cost = 0
        time = 0
        c = 0
        Source = ((cost, time, Src))
        heap.append(Source) # weight is cost basically
        Path.append((cost, time, Src, Src))
        print("------------PART ONE BELOW----------------")
        while heap:
            heap = self.poppedHeap(heap,Source)
            m = self.minValue(P[int(Source[2])])
            cost = m[int(0)]
            time = self.minTime(P[int(Source[2])])
            if len(P[int(Source[2])]) == 0 or Source[0] < cost or Source[1] < time:
                P[int(Source[2])].append(Source)
            out_edges = []
            for e in self.edges[Source[2]]:
                out_edges.append(e)
            for x in out_edges:
                m_tmp = self.minValue(P[int(x)])
                cost = m_tmp[0]
                time = self.minTime(P[int(x)])
                total_cost = int(Source[0]) + int(self.cost[Source[2], x])
                total_time = int(Source[1]) + int(self.time[Source[2], x])
                if len(P[int(x)]) == 0 or total_cost < cost or total_time < time:
                    adj_insert = (total_cost - int(Source[0]), total_time - int(Source[1]), x)
                    if adj_insert not in Adj[int(Source[2])]:
                        Adj[int(Source[2])].append((adj_insert))
                    heap.append((total_cost, total_time, x))
                    Path.append((total_cost, total_time, Source[2], x))        
            
            Source = self.minValue(heap)
        return P,Path,Adj 
        
        """      
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
                if int(tmp_cost) <= int(Budget):
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
        """



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
    
    p, path, adj = g.cost_option_algorithm(source,destination,budget)
    count = 0
    for a in adj:
        print("P[" + str(count) + "]  "+ str(a))
        count+=1
    count = 0
    for i in p:
        print("P[" + str(count) + "]  "+ str(i))
        count+=1
    shortest_path = g.pathFinder(path,destination,source,list())
    for r in reversed(shortest_path):
        print(" -> " + str(r),end='')
    print("\n\n")


if __name__ == "__main__":
    main(sys.argv[1:])
