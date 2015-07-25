'''
Created on 08/nov/2014

@author: Simone
'''
import threading
import snap
from snap import *

class ParallelRecDisp(threading.Thread):
    nodes = []
    dispersion_from_others = []
    G1 = TUNGraph.New()
    
    def __init__(self, nodes, dispersion_from_ohters, G1):
        super(ParallelRecDisp, self).__init__()
        self.nodes = nodes
        self.dispersion_from_others = dispersion_from_ohters
        self.G1 = G1
        
    def run(self):
        for n in self.dispersion_from_others:
            n = n+1
            print n
        