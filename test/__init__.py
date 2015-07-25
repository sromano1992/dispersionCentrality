'''
Created on 08/nov/2014

@author: Simone
'''
import thread
import time
import dispersion
import threading
import multiThreading
import snap
from snap import *

def loop1_10(node):
    for n in node:
        n = n + 1
    return node
 
nodes = [1, 2, 3, 4]
disp = [3,1,6,3]
G1 = TUNGraph.New()
for i in range(1,13):
    G1.AddNode(i)
node1 = []
node2 = []
i = 0
for tmp in nodes:
    if i<2:
        node1.append(tmp)
    if i>=2:
        node2.append(tmp)
    i = i+1

thread1 = multiThreading.ParallelRecDisp(node1, disp, G1)
thread1.start()
thread1.join(3)

for n in thread1.dispersion_from_others:
    print n,"_"