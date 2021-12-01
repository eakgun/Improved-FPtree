#Enes AKGYUN 2021

from collections import defaultdict, OrderedDict
from csv import reader
from itertools import chain, combinations
import matplotlib.pyplot as plt
import networkx as nx
import pickle
from networkx.generators.classic import ladder_graph
from fpGrowth import *
from graphUtils import *
import igraph as ig
import numpy as np
from igraph import Graph, EdgeSeq


def fpTreeFromFile(fname, minSupThreshold, minConf):
    itemSetList, counts = getFromFile(fname)
    minSup = len(itemSetList) * minSupThreshold
    fpTree, headerTable, itemSet = constructTree(itemSetList, counts, minSup)
    return fpTree, headerTable, itemSet
        


fpTree , headerTable, itemSet = fpTreeFromFile('tesco.csv',0.1,0.2)



fpTree.display()

#Drawing the FPtree

# paired_Set = [(u, v) for u in fpTree.lvld for v in fpTree.lvld if v-u == 1]  

pairs = list(enumerate(fpTree.lvld)) 
paired = [(u,v) for v, u in pairs]

pairedx = [(v,fpTree.lbl[v]+':'+str(fpTree.cnt[v])) for u,v in paired]

labeldict = {k:v for k,v in pairedx}

d = defaultdict(list)

for k,v in paired:
    d[k].append(v) 

new_pair = []

for i in range(1, len(d)):
    for j in range(len(d[i])):
        for k in range(len(d[i+1])):
            try:
                if d[i][j] < d[i+1][k] and d[i+1][k] < d[i][j+1]:
                    new_pair += [(d[i][j], d[i+1][k])]
            except:
                new_pair += [(d[i][j], d[i+1][k])]



#igraph vertex IDs starts from zero.
g = ig.Graph()
g.add_vertices(len(pairs))
g.add_edges(new_pair)
layout = g.layout_reingold_tilford(root=[0])
ig.plot(g, layout=layout)





