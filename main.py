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
from igraph import Graph, EdgeSeq


def fpTreeFromFile(fname, minSupThreshold, minConf):
    itemSetList, counts = getFromFile(fname)
    minSup = len(itemSetList) * minSupThreshold
    fpTree, headerTable, itemSet = constructTree(itemSetList, counts, minSup)
    return fpTree, headerTable, itemSet
        


fpTree , headerTable, itemSet = fpTreeFromFile('tesco.csv',0.1,0.2)


# tree.add_edge(ind,self.name)
# pos = hierarchy_pos(tree,1)

fpTree.display()

#Drawing the FPtree

# paired_Set = [(u, v) for u in fpTree.lvld for v in fpTree.lvld if v-u == 1]  

paired = list(enumerate(fpTree.lvld))

paired = [(u,v) for v, u in paired]
paired.pop(0)
pairedx = [(v,fpTree.lbl[v]+':'+str(fpTree.cnt[v])) for u,v in paired]

labeldict = {k:v for k,v in pairedx}

g = ig.Graph(n=12, directed=True)




# Tree = nx.Graph()
# Tree.add_edges_from(paired)
# pos = hierarchy_pos(Tree,1)
# nx.draw(Tree, pos=pos, labels=labeldict ,with_labels=True)

