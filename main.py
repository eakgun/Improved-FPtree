from collections import defaultdict, OrderedDict
from csv import reader
from itertools import chain, combinations
from fpGrowth import *



def fpTreeFromFile(fname, minSupThreshold, minConf):
    itemSetList, frequency = Node.getFromFile(fname)
    minSup = len(itemSetList) * minSupThreshold
    headerTable = constructTree(itemSetList, frequency, minSup)
    return headerTable