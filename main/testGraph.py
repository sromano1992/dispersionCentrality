'''
Created on 07/nov/2014

@author: Simone
'''
import datetime
import time
import dispersion
import snap
from snap import *


#G1 = snap.LoadEdgeList(snap.PUNGraph, "facebook_combined.txt", 0, 1)
#G1 = snap.LoadEdgeList(snap.PUNGraph, "0.edges", 0, 1)


G1 = TUNGraph.New()
for i in range(1,13):
    G1.AddNode(i)

G1.AddEdge(1,2)
G1.AddEdge(1,5)
G1.AddEdge(1,8)
G1.AddEdge(2,3)
G1.AddEdge(2,4)
G1.AddEdge(2,5)
G1.AddEdge(2,6)
G1.AddEdge(2,8)
G1.AddEdge(3,6)
G1.AddEdge(3,8)
G1.AddEdge(4,5)
G1.AddEdge(4,6)
G1.AddEdge(4,8)
G1.AddEdge(5,6)
G1.AddEdge(5,8)
G1.AddEdge(5,9)
G1.AddEdge(6,8)
G1.AddEdge(6,9)
G1.AddEdge(7,8)
G1.AddEdge(9,8)
G1.AddEdge(9,10)
G1.AddEdge(9,11)
G1.AddEdge(10,8)
G1.AddEdge(10,11)
G1.AddEdge(10,12)
G1.AddEdge(11,8)
G1.AddEdge(11,12)
G1.AddEdge(12,8)

current = datetime.datetime.now()
print dispersion.commonNeighbors(G1, 2, 10).Len()
#dispersion.recDisp(G1, 12, 3)
#dispersion.dispersion(G1, 2069, 1912)
#print datetime.datetime.now() - current 
#dispersion.recDisp(G1, 0, 3)
#print datetime.datetime.now() - current 
#dispersion.recDisp_immediate(G1, 8, 3)
