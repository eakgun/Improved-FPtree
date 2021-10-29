from collections import defaultdict, OrderedDict
from csv import reader
from itertools import chain, combinations
import matplotlib.pyplot as plt
import networkx as nx
import pickle
from fpGrowth import *
from graphUtils import *



def fpTreeFromFile(fname, minSupThreshold, minConf):
    itemSetList, counts = getFromFile(fname)
    minSup = len(itemSetList) * minSupThreshold
    fpTree, headerTable, itemSet = constructTree(itemSetList, counts, minSup)
    return fpTree, headerTable, itemSet
        


fpTree , headerTable, itemSet = fpTreeFromFile('tesco.csv',0.5,0.5)


# tree.add_edge(ind,self.name)
# pos = hierarchy_pos(tree,1)

fpTree.display()
