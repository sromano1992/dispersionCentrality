'''
Created on 10/nov/2014

@author: Simone
'''
import datetime
import time
import dispersion
import snap
from snap import *

G1 = snap.LoadEdgeList(snap.PUNGraph, "facebook_combined.txt", 0, 1)
dispersion.printNodesInformations_CSV(G1, "facebook_combined.csv", "all")