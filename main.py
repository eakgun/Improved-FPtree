from collections import defaultdict, OrderedDict
from csv import reader
from itertools import chain, combinations
from fpGrowth import Node as fp



def fpTreeFromFile(fname, minSupThreshold, minConf):
    itemSetList, frequency = fp.getFromFile(fname)
    minSup = len(itemSetList) * minSupThreshold
    headerTable = fp.constructTree(itemSetList, frequency, minSup)
    return headerTable