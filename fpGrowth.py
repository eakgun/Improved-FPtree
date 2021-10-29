from csv import reader
from collections import defaultdict
from itertools import chain, combinations
import networkx as nx
from graphUtils import *
import functools

class FPNode:
    def __init__(self, itemName, counts, parentNode):
        self.name = itemName
        self.count = counts
        self.parent = parentNode
        self.children = {}
        self.next = None
        self.indd = []

    def increment(self, counts):
        self.count += counts


    def display(self, ind=1):
        # print(ind, self.name, ' ', self.count)
        print(ind)
        self.indd += [ind]
        for child in list(self.children.values()):
        
            child.display(ind+1)
           

def getFromFile(fname):
    itemSetlist = []
    counts = [] 
    with open(fname, "r") as file:
        csv_reader = reader(file)
        for line in csv_reader:
            line = list(filter(None,line))
            itemSetlist.append(line)
            counts.append(1)

    return itemSetlist,counts


def constructTree(itemSetList, counts, minSup):
    headerTable = defaultdict(int)
    # (idx,itemSet) i.e. enumerate(itemSetList) = (0, ['a', 'c', 'd', 'f', 'g', 'i', 'm', 'p'])
    for idx, itemSet in enumerate(itemSetList):
        for item in itemSet:
            headerTable[item] += counts[idx]
    
    #delete below minsup
    headerTable = dict((item,sup) for item, sup in headerTable.items() if sup >= minSup)
    if(len(headerTable) == 0):
        return None,None

    for item in headerTable:
        headerTable[item] = [headerTable[item], None]
    #   ---headerTable---- [Item: [count, headNode]]
    # {'a': [3, None],
    # 'c': [4, None],
    # 'f': [4, None],
    # 'm': [3, None],
    # 'p': [3, None],
    # 'b': [3, None]}

    fpTree = FPNode('Null', 1, None)

    for idx, itemSet in enumerate(itemSetList):
        #item 
        itemSet = [item for item in itemSet if item in headerTable] #
        
        itemSet.sort(key=lambda item: headerTable[item][0], reverse=True)

        currentNode = fpTree
        for item in itemSet:
            currentNode = updateTree(item, currentNode, headerTable, counts[idx])
        
    return fpTree, headerTable, itemSet

def updateHeaderTable(item, targetNode, headerTable):

    if(headerTable[item][1] == None):
        headerTable[item][1] = targetNode
    else:
        currentNode = headerTable[item][1]
        #go to the end node then link the target
        #traverse until its None (meaning the end of the linked list)
        while currentNode.next != None:
            currentNode = currentNode.next
        currentNode.next = targetNode




def updateTree(item, treeNode, headerTable, counts):

    if item in treeNode.children:
        treeNode.children[item].increment(counts)
    else:
        #new Branch
        newItemNode = FPNode(item, counts, treeNode)
        treeNode.children[item] = newItemNode
        #Link it to the headerTable
        updateHeaderTable(item, newItemNode, headerTable)

    return treeNode.children[item]


def mineFP(headerTable, minSup, preFix, freqItemList):
    #Sort by count and create a list
    sortedItemList = [item[0] for item in sorted(list(headerTable.items()), key=lambda p: p[1][0])]
    # Start with the lowest support
    for item in sortedItemList:
     # Pattern growth is achieved by the concatenation of suffix pattern with 
     # frequent patterns generated from conditional FP-tree
     newFreqSet = preFix.copy()
     newFreqSet.add(item)
     freqItemList.append(newFreqSet)
     #Find all prefix path, construct conditional pattern base
     conditionalPatternBase, counts = findPrefixPath(item, headerTable)
     #construct conditional FP tree with cond patt base
     conditionalTree, newHeaderTable = constructTree(conditionalPatternBase, counts, minSup)
     if newHeaderTable !=None:
         #Recursively mine on the tree
         mineFP(newHeaderTable, minSup, preFix, freqItemList)


def findPrefixPath(basePattern, headerTable):
    #First node in the linked list
    treeNode = headerTable[basePattern][1]
    condPatterns = []
    counts = []
    while treeNode != None:
        prefixPath = []
        # from leaf node all the way to the root
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            #Store the path and the count
            condPatterns.append(prefixPath[1:])
            counts.append(treeNode.count)
        
        #next node
        treeNode = treeNode.next

    return condPatterns, counts

def ascendTree(node, prefixPath):
    if node.parent != None:
        prefixPath.append(node.name)
        ascendTree(node.parent, prefixPath)

# ---ItemSetList---    
#  [['a', 'c', 'd', 'f', 'g', 'i', 'm', 'p'],
#   ['a', 'b', 'c', 'f', 'i', 'm', 'o'],
#   ['b', 'f', 'h', 'j', 'o'],
#   ['b', 'c', 'k', 's', 'p'],
#   ['a', 'c', 'e', 'f', 'l', 'm', 'n', 'p']]

# ---HeaderTable---
# {'a': [3, None],
#   'c': [4, None],
#   'f': [4, None],
#   'm': [3, None],
#   'p': [3, None],
#   'b': [3, None]}

# ---Counts----
# [1, 1, 1, 1, 1]