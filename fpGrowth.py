from csv import reader
from collections import defaultdict
from itertools import chain, combinations
import igraph as ig
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

    def capture(self,lvl,lvld,lbl,cnt):
        
        lvld += [lvl] 
        lbl += [self.name]
        cnt += [self.count]
        
        

    def fpPlot(self, fname):
        
        #Drawing the FPtree
        self.stats()
        # paired_Set = [(u, v) for u in fpTree.lvld for v in fpTree.lvld if v-u == 1]
       
        pairs = []
        pairs = list(enumerate(self.lvld)) 
        print(pairs)
        paired = [(u,v) for v, u in pairs]
        pairedx = [(v,self.lbl[v]+':'+str(self.cnt[v])) for u,v in paired]
        
        print(self.lvld)
        print(pairs)
        
        
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


        labels = [u for v,u in pairedx]


        #igraph vertex IDs starts from zero.
        print(pairs)
        g = ig.Graph()
        g.add_vertices(len(pairs))
        g.add_edges(new_pair)
        g.vs["label"] = labels
        visual_style = {}
        visual_style["vertex_size"] = 40
        visual_style["vertex_color"] = "#4d4dff"
        visual_style["vertex_label_color"] = "white"
        layout = g.layout_reingold_tilford(root=[0])
        
        return g, visual_style, layout

    def increment(self, counts):
        self.count += counts

    # def lvlCount(lvl):
    #     self.lvld += [lvl]
    
    def stats(self, lvl=1):
        print(lvl ,' '*lvl, self.name, ' ', self.count)
        self.capture(lvl,self.lvld,self.lbl,self.cnt)

        for child in list(self.children.values()):
            child.stats(lvl+1)
           

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