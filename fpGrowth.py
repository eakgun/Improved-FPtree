from csv import reader
from collections import defaultdict
from itertools import chain, combinations

class Node:
    def __init__(self, itemName, frequency, parentNode):
        self.name = itemName
        self.count = frequency
        self.parent = parentNode
        self.children = {}
        self.next = None

    def increment(self, frequency):
        self.count += frequency
        
    def getFromFile(fname):
        itemSetlist = []
        frequency = [] 
        with open(fname, "r") as file:
            csv_reader = reader(file)
            for line in csv_reader:
                line = list(filter(None,line))
                itemSetlist.append(line)
                frequency.append(1)

        return itemSetlist,frequency


def constructTree(itemSetList, frequency, minSup):
    headerTable = defaultdict(int)
    # (idx,itemSet) i.e. (0, ['a', 'c', 'd', 'f', 'g', 'i', 'm', 'p'])
    for idx, itemSet in enumerate(itemSetList):
        for item in itemSet:
            headerTable[item] += frequency[idx]
    
    #delete below minsup
    headerTable = dict((item,sup) for item, sup in headerTable.items() if sup >= minSup)
    if(len(headerTable) == 0):
        return None,None

    for item in headerTable:
        headerTable[item] = [headerTable[item], None]
    

    fpTree = Node('Null', 1, None)

    for idx, itemSet in enumerate(itemSetList):
        itemSet = [item for item in itemSet if item in headerTable] #list comprehension
        itemSet.sort(key=lambda item: headerTable[item][0], reverse=True)

        currentNode = fpTree
        for item in itemSet:
            currentNode = updateTree(item, currentNode, headerTable, frequency)

def updateHeaderTable(item, targetNode, headerTable):

    if(headerTable)


    return 



def updateTree(item, treeNode, headerTable, frequency):
    if item in treeNode.children:
        treeNode.children[item].increment(frequency)
    else:
        #new Branch
        newItemNode = Node(item, frequency, treeNode)
        treeNode.children[item] = newItemNode
        #Link it to the headerTable
        updateHeaderTable(item, newItemNode, headerTable)

    return treeNode.children[item]






    

    