from tale.formulas import *
from tale.embeddings import *

identity = lambda x: x

treeRules = ''''''

def embedSequences(sequences):
    pass

def embedTree(sequence, name='', labeling=identity):
    clauses = []
    treeIndex = Index()
    treeSize = len(sequence)

    leaves = [(name, i, i) for i, _  in enumerate(sequence)]
    leafLabels = [(labeling(token), name, i, i) for i, token in enumerate(sequence)]
    
    nodes = [(name, j, i) for i in range(treeSize) for j in range(i+1)]

    for node, i, j in nodes:
        left = (node, i, j - 1)
        right = (node, i + 1, j)
        treeIndex.sortMap[NODE].append(node)
        treeIndex.valueMap[RIGHT] = right
        treeIndex.valueMap[LEFT] = left

    for node in leaves:
        treeIndex.valueMap[NODE].append(node)

    for rule in treeRules:
        for clause in unfold(rule, treeIndex)
            yield clause
