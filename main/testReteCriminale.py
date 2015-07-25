'''
Created on 20/nov/2014

@author: Simone
'''

import datetime
import time
import dispersion
import snap
from snap import *

dispersion.fromGexfToEdge("reteCriminale.gexf", "reteCriminale.edge");
G1 = snap.LoadEdgeList(snap.PUNGraph, "reteCriminale.edge", 0, 1)

current = datetime.datetime.now()
#dispersion.printNodesInformations(G1, 1)
dispersion.printNodesInformations_XML(G1, "reteCriminale.xml", "all")
dispersion.printNodesInformations_CSV(G1, "reteCriminale.csv", "all")