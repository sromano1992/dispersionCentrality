# da ottimizzare

import snap
import re
from snap import *
import logging
from fileinput import filename

def fromGexfToEdge(inputFileName, outputFileName):
    inputfile = open(inputFileName)
    outputfile = open(outputFileName, 'w')
    
    nodi = {}
    count = 0
    for i in range(1): inputfile.next()  # skip first four lines
    for line in inputfile:
        try:
            found = re.search('<node id="(.+?)" ', line).group(1)
            nodi[found] = count
            count += 1
        except AttributeError:
            # AAA, ZZZ not found in the original string
            found = ''  # apply your error handling
        try:
            found1 = re.search('source="(.+?)" ', line).group(1)
            found2 = re.search('target="(.+?)" ', line).group(1)
            string = str(nodi[found1]) + " " + str(nodi[found2]) + "\n"
            outputfile.write(string)
        except AttributeError:
            # AAA, ZZZ not found in the original string
            found = ''  # apply your error handling
    outputfile1 = open(outputFileName+"_correspondence.txt", 'w')
    outputfile1.write(str(nodi))
    
    inputfile.close()
    outputfile.close()
    
def inductGraph(G1, u):
    #crea il grafo indotto (vicinato) di u
    nodes = snap.TIntV()

    for N in G1.GetNI(u).GetOutEdges():
        nodes.Add(N)
    SubGraph1 = snap.GetSubGraph(G1, nodes)
    return SubGraph1
    
def commonNeighbors(G1, u, h):
    a = set()
    b = set()
    for N in G1.GetNI(u).GetOutEdges():
        a.add(N)
    for N in G1.GetNI(h).GetOutEdges():
        b.add(N)
    intersect = a.intersection(b)
    nodes = snap.TIntV()
    for n in intersect:
        nodes.Add(n)
    return nodes


def dispersion(G1, u=8, h=9):
    #logging.basicConfig(level=logging.DEBUG)

    logging.debug(str(type(u)) + str(type(h)))
    if (not (G1.IsEdge(u, h))):
        #print "non c'e l'arco tra u e h"
        return

    nodes = commonNeighbors(G1, u, h)

    #print "doing something"

    sum = 0
    for i in nodes:
        for j in nodes:

            if i < j:
                logging.debug(str(i) + " " + str(j) + " - " + str(G1.IsEdge(i, j)))
                if (not (G1.IsEdge(i, j))):
                    logging.debug("non c'e l'arco")
                    nodes1 = snap.TIntV()
                    for N in G1.GetNI(i).GetOutEdges():
                        nodes1.Add(N)

                    #rimuovi il nodo u e h dalla lista dei nodi
                    nodes1.DelAll(u)
                    nodes1.DelAll(h)
                    Sub1 = snap.GetSubGraph(G1, nodes1)

                    nodes2 = snap.TIntV()
                    for N in G1.GetNI(j).GetOutEdges():
                        nodes2.Add(N)

                    #rimuovi il nodo u e h dalla lista dei nodi
                    nodes2.DelAll(u)
                    nodes2.DelAll(h)
                    #Sub2 = snap.GetSubGraph(G1, nodes2)

                    flag = 0
                    for k in nodes1:
                        for l in nodes2:
                            if (k == l):
                                flag = 1

                    if (flag == 0):
                        #logging.debug(str(k) +" " + str(l) + "......")
                        sum = sum + 1
                        logging.debug("sum: " + str(sum))

    #print "la dispersione tra il numero u e il nodo h e': ", sum
    return float(sum)


def embeddedness(G1, u=8, h=9):
    #logging.basicConfig(level=logging.DEBUG)

    logging.debug(str(type(u)) + str(type(h)))
    if (not (G1.IsEdge(u, h))):
        #print "non c'e l'arco tra u e h"
        return

    nodes = commonNeighbors(G1, u, h)

    #print "la embeddedness e'", nodes.Len()
    return nodes.Len()


def norm(G1, u=8, h=9):
    #logging.basicConfig(level=logging.DEBUG)

    logging.debug(str(type(u)) + str(type(h)))
    if (not (G1.IsEdge(u, h))):
        return  #dispersion between u and h cannot be calculated

    dispers = dispersion(G1, u, h)
    emb = embeddedness(G1, u, h)
    
    if emb == 0:
        return float(0)
    normaliz = float(dispers) / float(emb)
    #print "la norma e' %.5f" % normaliz
    return normaliz


def performance(G1, a=0.61, b=0, c=5, u=8, h=9):
    #logging.basicConfig(level=logging.DEBUG)

    logging.debug(str(type(u)) + str(type(h)))
    if (not (G1.IsEdge(u, h))):
        #print "non c'e l'arco tra u e h"
        return

    dispers = dispersion(G1, u, h)
    emb = embeddedness(G1, u, h)
    perf = ((dispers + b) ** a) / float((emb + c))
    print "la performance e'", perf
    return perf

    
#use new value of Xv in next iterations
def recDisp(G1, u, num_iterations):
    indGraph = inductGraph(G1, u)
    dispersionFromOthers = {}   #contains node=Xnode
    dispersionFromOthers_tmp = {}
    
    #Xi = 1 for all node i near u
    for node in indGraph.Nodes():
        dispersionFromOthers[node.GetId()] = 1   
        dispersionFromOthers_tmp[node.GetId()] = 1
        
    #start iterations
    iteration = 0
    while iteration < num_iterations:
        print "Iteration: ", iteration + 1
        for node in indGraph.Nodes():
            Cuv = commonNeighbors(G1, u, node.GetId())
            #calculate first term of sum
            first_term = 0
            for xi in Cuv:
                first_term = first_term + dispersionFromOthers[xi]**2
            #calculate second term of sum
            second_term = 0
            for i in Cuv:
                for j in Cuv:
                    if i<j:
                        if (not G1.IsEdge(i,j) and have_common_neighbors(G1, i, j, u, node.GetId()) == 0):
                            second_term = second_term + (1*dispersionFromOthers[i]*dispersionFromOthers[j])
            #calculate value Xi
            if (embeddedness(G1, u, node.GetId())): #embeddendness not 0
                dispersionFromOthers_tmp[node.GetId()] = (first_term + (2 * second_term))/embeddedness(G1, u, node.GetId())
                print node.GetId(), " ", dispersionFromOthers_tmp[node.GetId()]
        for node in indGraph.Nodes():
            dispersionFromOthers[node.GetId()] = dispersionFromOthers_tmp[node.GetId()] 
        iteration = iteration + 1
        
#use new value of Xv immediatly
def recDisp_immediate(G1, u, num_iterations):
    indGraph = inductGraph(G1, u)
    dispersionFromOthers = {}   #contains node=Xnode
    dispersionFromOthers_tmp = {}
    
    #Xi = 1 for all node i near u
    for node in indGraph.Nodes():
        dispersionFromOthers[node.GetId()] = 1   
        
    #start iterations
    iteration = 0
    while iteration < num_iterations:
        print "Iteration: ", iteration + 1
        for node in indGraph.Nodes():
            Cuv = commonNeighbors(G1, u, node.GetId())
            #calculate first term of sum
            first_term = 0
            for xi in Cuv:
                first_term = first_term + dispersionFromOthers[xi]**2
            #calculate second term of sum
            second_term = 0
            for i in Cuv:
                for j in Cuv:
                    if i<j:
                        if (not G1.IsEdge(i,j) and have_common_neighbors(G1, i, j, u, node.GetId()) == 0):
                            second_term = second_term + (1*dispersionFromOthers[i]*dispersionFromOthers[j])
            #calculate value Xi
            if (embeddedness(G1, u, node.GetId())): #embeddendness not 0
                dispersionFromOthers[node.GetId()] = (first_term + (2 * second_term))/embeddedness(G1, u, node.GetId())
                print node.GetId(), " ", dispersionFromOthers[node.GetId()]
        iteration = iteration + 1

#i and j haven't common neighbors except u and h in graph G1 
def have_common_neighbors(G1, i, j, u, h):
    nodes1 = snap.TIntV()
    for N in G1.GetNI(i).GetOutEdges():
        nodes1.Add(N)

    #rimuovi il nodo u e h dalla lista dei nodi
    nodes1.DelAll(u)
    nodes1.DelAll(h)
    Sub1 = snap.GetSubGraph(G1, nodes1)

    nodes2 = snap.TIntV()
    for N in G1.GetNI(j).GetOutEdges():
        nodes2.Add(N)

    #rimuovi il nodo u e h dalla lista dei nodi
    nodes2.DelAll(u)
    nodes2.DelAll(h)
    #Sub2 = snap.GetSubGraph(G1, nodes2)

    flag = 0
    for k in nodes1:
        for l in nodes2:
            if (k == l):
                flag = 1

    if (flag == 0):
        return 0
    return 1
                        
def printInfo(G):
    snap.PrintInfo(G, "Python type PUNGraph")

def useOfDictionary():
    streetno = { "1" : "Sachin Tendulkar",
            2 : "Dravid",
            "3" : "Sehwag",
            4 : "Laxman",
            5 : "Kohli" }
    streetno[1] = 3
    
    for keys,values in streetno.items():
        print(keys)
        print(values)
    print streetno
    print streetno[1]
    
def printNodesInformations(G1, node):
    Nodes = snap.TIntFltH()
    Edges = snap.TIntPrFltH()
    snap.GetBetweennessCentr(G1, Nodes, Edges, 1.0)
    
    #dispersion from others nodes
    print "Report for node ", node
    print "1)DISPERSION"
    for n in G1.Nodes():
        if n.GetId() != node:
            print "dispersion of ", node, " from ", n.GetId(), " = ", norm(G1, node, n.GetId())
    print "2)DEGREE CENTRALITY"
    print GetDegreeCentr(G1, node)
    print "3)CLOSENESS CENTRALITY"
    print GetClosenessCentr(G1,node)
    print "4)BETWEENNESS CENTR"
    print Nodes[node]

#print xml info for only one node
def printNodeInformations_XML(G1, node, fileName):
    out_file = open(fileName,"w")
    
    Nodes = snap.TIntFltH()
    Edges = snap.TIntPrFltH()
    snap.GetBetweennessCentr(G1, Nodes, Edges, 1.0)
    
    out_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    #dispersion from ,others nodes
    out_file.write("<node>"+str(node)+"</node>\n")
    out_file.write("<degree_centrality>"+str(GetDegreeCentr(G1, node))+"</degree_centrality>\n")
    out_file.write("<closeness_centrality>"+str(GetClosenessCentr(G1,node))+"</closeness_centrality>\n")
    out_file.write("<betweenness_centrality>"+str(Nodes[node])+"</betweenness_centrality>\n")
    for n in G1.Nodes():
        if n.GetId() != node:
            out_file.write("<dispersion from='"+str(n.GetId())+"'>"+str(norm(G1, node, n.GetId()))+"</dispersion>\n")
    out_file.close()

#print xml info for first numNode nodes in graph
#if numNode == "all" print info for all nodes
def printNodesInformations_XML(G1, fileName, numNode):
    print "start node information creating..."
    out_file = open(fileName,"w")
    xsl_file_name = fileName+".xsl"
    
    Nodes = snap.TIntFltH()
    Edges = snap.TIntPrFltH()
    snap.GetBetweennessCentr(G1, Nodes, Edges, 1.0)
    #kMax = getKmax(G1)
    
    out_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    out_file.write("<?xml-stylesheet type=\"text/xsl\" href=\"graphic_xsl.xsl\"?>\n")
    out_file.write("<nodes>\n")
    i=0
    #all info for each nodes
    for node in G1.Nodes():
        if numNode != "all":
            if i >= numNode:
                out_file.write("</nodes>\n")
                return
            i = i+1
        print "info for node: " + str(node.GetId())
        out_file.write("\t<node id='"+str(node.GetId())+"'>\n")
        out_file.write("\t\t<degree_centrality>"+str(GetDegreeCentr(G1, node.GetId()))+"</degree_centrality>\n")
        out_file.write("\t\t<closeness_centrality>"+str(GetClosenessCentr(G1,node.GetId()))+"</closeness_centrality>\n")
        out_file.write("\t\t<betweenness_centrality>"+str(Nodes[node.GetId()])+"</betweenness_centrality>\n")
        #for n in G1.Nodes():
        #    if n.GetId() != node.getId():
        #        dispersion = norm(G1, node.GetId(), n.GetId())
        #        if dispersion != None:
        #           out_file.write("\t\t<dispersion from='"+str(n.GetId())+"'>"+str(norm(G1, node.GetId(), n.GetId()))+"</dispersion>\n")
        out_file.write("\t\t<dispersion_centrality>"+str(dispersionCentrality(G1, node.GetId()))+"</dispersion_centrality>\n")
        #out_file.write("\t\t<normalized_dispersion_centrality>"+str(normalizedDispersionCentrality(G1, node.GetId(),kMax))+"</normalized_dispersion_centrality>\n")
        out_file.write("\t\t<dispersion_average>"+str(avg_dispersion(G1, node.GetId()))+"</dispersion_average>\n") 
        out_file.write("\t\t<dispersion_max>"+str(max_dispersion(G1, node.GetId()))+"</dispersion_max>\n") 
        out_file.write("\t\t<dispersion_min>"+str(min_dispersion(G1, node.GetId()))+"</dispersion_min>\n") 
        out_file.write("\t</node>\n")
    out_file.write("</nodes>\n")
    out_file.close()
    
    #generation of xsl to show result in browser
    generateXsl(xsl_file_name)

#for an input node calculate its dispersion from others node
#in G1 and normalize it between 0 and 1;
#then calculate mediumn between all dispersion
#kMax is max
def dispersionCentrality(G1, u):
    number = 0
    dispersionCentrality = 0
    
    for n in G1.Nodes():
        if n.GetId() != u:
            disp = dispersion(G1, u, n.GetId())
            if disp != None:
                dispersionCentrality = dispersionCentrality + (float(disp))#/float(divisor))
    
    return dispersionCentrality
    
#reutrn number of biggest neighbors in graph
#checking between each pairs of nodes
def getKmax(G1):
    kMax = 0
    for node1 in G1.Nodes():
        for node2 in G1.Nodes():
            if node2.GetId() > node1.GetId():
                newK = commonNeighbors(G1, node1.GetId(), node2.GetId()).Len()
                if newK > kMax:
                    kMax = newK
    return kMax


#for an input node calculate its dispersion from others node
#in G1 and normalize it between 0 and 1;
#then calculate mediumn between all dispersion
#kMax is max
def normalizedDispersionCentrality(G1, u, kMax):
    number = 0
    dispersionCentrality = 0
    divisor = 2**int(kMax)   #normalization coefficient
    
    sumOfDispersion = 0.0
    for n in G1.Nodes():
        if n.GetId() != u:
            disp = norm(G1, u, n.GetId())
            if disp != None:
                sumOfDispersion = sumOfDispersion + (disp/float(divisor))
    
    for n in G1.Nodes():
        if n.GetId() != u:
            disp = dispersion(G1, u, n.GetId())
            if disp != None:
                dispersionCentrality = dispersionCentrality + (float(disp))/float(divisor)
    
    return dispersionCentrality


#return the average of all u's dispersions
#from others node in G1
def avg_dispersion(G1, u):
    number = 0
    sum_dispersion = 0
    
    for n in G1.Nodes():
        if n.GetId() != u:
            disp = dispersion(G1, u, n.GetId())
            if disp != None:
                number = number + 1
                sum_dispersion = sum_dispersion + disp
    
    if number != 0:
        return sum_dispersion / number
    return sum_dispersion

def min_dispersion(G1, u):
    min = 0
    
    for n in G1.Nodes():
        if n.GetId() != u:
            isMin = dispersion(G1,u,n.GetId())
            if (isMin != None and isMin<min):
                min = isMin

    return min

def max_dispersion(G1, u):
    max = 0
    
    for n in G1.Nodes():
        if n.GetId() != u:
            isMax = dispersion(G1,u,n.GetId())
            if (isMax != None and isMax>max):
                max = isMax

    return max

def generateXsl(xslFileName):
    print "Xsl Not implemented yet"
    
#from xml generated to csv for gephi
def printNodesInformations_CSV(G1, fileName, numNode):
    print "start node information creating..."
    out_file = open(fileName,"w")
    
    Nodes = snap.TIntFltH()
    Edges = snap.TIntPrFltH()
    print "calculating BetweennessCentr..."
    snap.GetBetweennessCentr(G1, Nodes, Edges, 0.99)
    #kMax = getKmax(G1)
    
    out_file.write("id,closeness_centrality,betweenness_centrality,dispersion_centrality\n")
    i=0
    #all info for each nodes
    for node in G1.Nodes():
        if numNode != "all":
            if i >= numNode:
                return
            i = i+1
        print "info for node: " + str(node.GetId())
        out_file.write(str(node.GetId())+",")
        #out_file.write(str(GetDegreeCentr(G1, node.GetId()))+",")
        out_file.write(str(GetClosenessCentr(G1,node.GetId()))+",")
        out_file.write(str(Nodes[node.GetId()])+",")    #betweenness_centrality
        #print "betweenness ok...";
        out_file.write(str(dispersionCentrality(G1, node.GetId()))+"\n")
        #out_file.write(str(avg_dispersion(G1, node.GetId()))+",") 
        #out_file.write(str(max_dispersion(G1, node.GetId()))+",") 
        #out_file.write(str(min_dispersion(G1, node.GetId()))+"\n") 
    out_file.close()    
    #generation of xsl to show result in browser
    #generateXsl(xsl_file_name)
    
def compare_betweenness_centrality(G1, fileName):
    print "start betweenness comparison creating..."
    out_file = open(fileName,"w")
    Nodes = snap.TIntFltH()
    Edges = snap.TIntPrFltH()
    out_file.write("id,betweenness_centrality,approx\n")
    approx = float(1)
    for approx in range(1,10):
        snap.GetBetweennessCentr(G1, Nodes, Edges, float(approx)/10)
        print "creating info for approx = " + str(float(approx)/10)
        for node in G1.Nodes():
            out_file.write(str(node.GetId())+",")
            out_file.write(str(Nodes[node.GetId()])+",")
            out_file.write(str(float(approx)/10)+"\n")
        approx = approx + 0.1
    out_file.close()

def printAllNodes(G1):
     for node in G1.Nodes():
        print "info for node: " + str(node.GetId())

