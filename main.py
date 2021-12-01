#Enes AKGYUN 2021

from collections import defaultdict, OrderedDict
from csv import reader
from tkinter.constants import N
import matplotlib.pyplot as plt
from traitlets.traitlets import default
from fpGrowth import *
import igraph as ig
import numpy as np


def fpTreeFromFile(fname, minSupThreshold, minConf):
    itemSetList, counts = getFromFile(fname)
    minSup = len(itemSetList) * minSupThreshold
    fpTree, headerTable, itemSet = constructTree(itemSetList, counts, minSup)
    
    
    return fpTree, headerTable, itemSet
        


















# def fpPlot(fname):

#     #Drawing the FPtree

#     # paired_Set = [(u, v) for u in fpTree.lvld for v in fpTree.lvld if v-u == 1]  

#     pairs = list(enumerate(fpTree.lvld)) 
    
#     paired = [(u,v) for v, u in pairs]

#     pairedx = [(v,fpTree.lbl[v]+':'+str(fpTree.cnt[v])) for u,v in paired]
 
   
#     print(fpTree.lvld)
    
#     d = defaultdict(list)

#     for k,v in paired:
#         d[k].append(v) 

#     new_pair = []

#     for i in range(1, len(d)):
#         for j in range(len(d[i])):
#             for k in range(len(d[i+1])):
#                 try:
#                     if d[i][j] < d[i+1][k] and d[i+1][k] < d[i][j+1]:
#                         new_pair += [(d[i][j], d[i+1][k])]
#                 except:
#                     new_pair += [(d[i][j], d[i+1][k])]


#     labels = [u for v,u in pairedx]


#     #igraph vertex IDs starts from zero.
#     print(pairs)
#     g = ig.Graph()
#     g.add_vertices(len(pairs))
#     pairs = None
#     g.add_edges(new_pair)
#     g.vs["label"] = labels
#     visual_style = {}
#     visual_style["vertex_size"] = 40
#     visual_style["vertex_color"] = "#4d4dff"
#     visual_style["vertex_label_color"] = "white"
#     layout = g.layout_reingold_tilford(root=[0])
    
   
#     new_pair =None
#     labels = None
#     d = None

#     return g, layout, visual_style
