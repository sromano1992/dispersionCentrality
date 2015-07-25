'''
Created on 10/nov/2014

@author: Simone
'''
import datetime
import time
import dispersion
import snap
from snap import *

G1 = snap.LoadEdgeList(snap.PUNGraph, "karate.txt", 0, 1)

current = datetime.datetime.now()
#dispersion.printNodesInformations(G1, 1)
#dispersion.printNodesInformations_XML(G1, "karate_node.xml", "all")
#dispersion.printNodesInformations_CSV(G1, "karate.csv", "all")
dispersion.compare_betweenness_centrality(G1, "facebook_betweenness_approx.csv")