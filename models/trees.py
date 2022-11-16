from tale.formulas import *
from tale.embeddings import *

identity = lambda x: x

NODE = 'node'
LABEL = 'label'

scaffolding = '''
either leaf (a), node (a).
either actual (a), virtual (a).

not leftnode (a), not rightnode (a) -> not directed (a).
not directed (a), virtual (a) -> False.

leftnode (a) -> directed (a).
rightnode (a) -> directed (a).
directed (a), actual (a) -> False.

leftnode (a), terminal (a.left, A) -> terminal (a, A).
rightnode (a), terminal (a.right, A) -> terminal (a, A).

actual (a), terminal (a.left, A) <-> leftTerminal (a, A).
actual (a), terminal (a.right, A) <-> rightTerminal (a, A).
'''

longRule = lambda l,r,h : f"leftTerminal (a, {l}), rightTerminal (a, {r}) -> terminal (a, {h}).\n"
shortRule = lambda h, p : f"symbol (a, {p}) -> terminal (a, {h}).\n"

def embedSequences(sequences, tokenLabeling):
    for sequence, identifier in sequences:
        for clause in embedTree(sequence, name=identifier, labeling=tokenLabeling):
            yield clause

def parseGrammar(text):

    grammar = ""
    preterminals = set()

    lines = [line.strip() for line in text.split("\n")]

    lastHead = ""
    ruleCount = 1

    for line in lines:

        ruleCount += 1
        i = ruleCount

        noHead = "->" == line[0:2]
        line = line.replace("->", "", 1)
        tokens = [token.strip() for token in line.split()]

        if len(tokens) == 3 and not noHead:
            head, left, right = tuple(tokens)
            last = str(head)
            line = longRule(left, right, head)
            grammar = grammar_spec + line
            preterminals.add(head)
            preterminals.add(left)
            preterminals.add(right)

        if len(tokens) == 2 and noHead:
            left, right = tuple(tokens)
            head = lastHead
            line = longRule(left, right, head)
            grammar = grammar_spec + line
            preterminals.add(head)
            preterminals.add(left)
            preterminals.add(right)

        if len(tokens) == 2 and not noHead:
            head, right = tuple(tokens)
            last = head
            line = shortRule(head, right)
            grammar = grammar + line
            preterminals.add(head)
            preterminals.add(left)
            preterminals.add(right)

        if len(tokens) == 1 and noHead:
            right = tokens[0]
            head = lastHead
            line = shortRule(head, right)
            grammar = grammar + line
            preterminals.add(head)
            preterminals.add(left)
            preterminals.add(right)

    return grammar, preterminals

def embedTree(sequence, grammar, name='', labeling=identity):
    clauses = []
    treeIndex = Index()
    size = len(sequence)
    productions, labels = parseGrammar(grammar)
    rules = parseProgram(scaffolding) + productions

    leaves = [(name, i, i) for i, _  in enumerate(sequence)]
    leafLabels = [(labeling(token), name, i, i) for i, token in enumerate(sequence)]
    
    nodes = [(name, j, i) for i in range(size) for j in range(i+1)]

    for node, i, j in nodes:
        left = (node, i, j - 1)
        right = (node, i + 1, j)
        treeIndex.sortMap[NODE].append(node)
        treeIndex.valueMap[RIGHT] = right
        treeIndex.valueMap[LEFT] = left

    for leafLabel in leafLabels:
        pass

    for clause in oneOf(labels, nodes):
        yield clause

    for node in leaves:
        treeIndex.valueMap[NODE].append(node)

    for label in labels:
        treeIndex.valueMap[LABEL].append(label)

    nodeVariable = 'a'
    labelVariable = 'A'
    treeIndex.variableMap[nodeVariable] = NODE
    treeIndex.variableMap[labelVariable] = LABEL

    for rule in rules:
        for clause in unfold(rule, treeIndex)
            yield clause
