from tale.formulas import *
from tale.embeddings import *

identity = lambda x: x

NODE = 'node'
LABEL = 'label'

longRule = lambda l, r, h: f"leftTerminal (a, {l}), rightTerminal (a, {r}) -> terminal (a, {h}).\n"
shortRule = lambda h, p: f"symbol (a, {p}) -> terminal (a, {h}).\n"
nodeName = lambda n, i, j: f"{n}[{i},{j}]"


def embedSequences(sequences, tokenLabeling):
    for sequence, identifier in sequences:
        for clause in embedTree(sequence,
                                name=identifier,
                                labeling=tokenLabeling):
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


def embedTree(sequence, grammar, name='', customLabels=[], labeling=identity):
    clauses = []
    treeIndex = Index()
    size = len(sequence)
    productions, labels = parseGrammar(grammar)
    rules = parseProgram(scaffolding) + productions

    leaves = [(name, i, i) for i, _ in enumerate(sequence)]
    leafLabels = [(labeling(token), name, i, i)
                  for i, token in enumerate(sequence)]

    nodes = [(name, j, i) for i in range(size) for j in range(i + 1)]

    for node, i, j in nodes:
        left = (node, i, j - 1)
        right = (node, i + 1, j)
        nodeName = nodeString(name, i, j)
        leftName = nodeString(*left)
        rightName = nodeString(*right)
        treeIndex.sortMap[NODE].append(nodeName)
        treeIndex.valueMap[RIGHT] = rightName
        treeIndex.valueMap[LEFT] = leftName

    for label, name, i, j in leafLabels:
        nodeName = nodeString(name, i, j)
        yield Atom(termify(label, nodeName))

    for clause in oneOf(labels, nodes):
        yield clause

    for node in leaves:
        treeIndex.valueMap[NODE].append(node)

    if not customLabels:
        for label in labels:
            treeIndex.valueMap[LABEL].append(label)

    nodeVariable = 'a'
    labelVariable = 'A'
    treeIndex.variableMap[nodeVariable] = NODE
    treeIndex.variableMap[labelVariable] = LABEL

    for rule in rules:
        for clause in unfold(rule, treeIndex):
            yield clause
