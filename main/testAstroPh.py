'''
Created on 10/nov/2014

@author: Simone
'''
import datetime
import time
import dispersion
import snap
from snap import *

G1 = snap.LoadEdgeList(snap.PUNGraph, "AstroPh.txt", 0, 1)
dispersion.printNodesInformations_CSV(G1, "AstroPh.csv", "all")