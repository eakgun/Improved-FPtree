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
        
    lvld = []
    lbl = []
    cnt = []
    def increment(self, counts):
        self.count += counts

    # def lvlCount(lvl):
    #     self.lvld += [lvl]

    def display(self, lvl=1):
        print(lvl ,' '*lvl, self.name, ' ', self.count)
        
        self.lvld += [lvl] 
        self.lbl += [self.name]
        self.cnt += [self.count]
        for child in list(self.children.values()):
        
            child.display(lvl+1)
           

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