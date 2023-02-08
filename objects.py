NEWLINE = "\n"


class BrokenPrecondition(Exception):

    def __init__(self, message, data={}):
        self.message = message
        self.data = data

    def __str__(self):
        return self.message

    def __bool__(self):
        return True


def remainder(vertex, left, right):
    left = {(a, b) for a, b in left if a != vertex}
    right = {(a, b) for a, b in right if a != vertex}
    return left, right


def successors(vertex, relation):
    successors = {b for a, b in relation if a == vertex}
    return successors


def bort(vertex, left, right):
    leftSuccessors = successors(vertex, left)
    rightSuccessors = successors(vertex, right)

    if len(leftSuccessors) == 0 and len(rightSuccessors) == 0:
        return Leaf(vertex)

    if len(leftSuccessors) == 1:
        leftChild = leftSuccessors.pop()
    elif len(leftSuccessors) > 1:
        raise BrokenPrecondition(
            f"More than one left successor found for vertex {vertex}")
    elif len(leftSuccessors) == 0:
        raise BrokenPrecondition(
            f"No left successor found for vertex {vertex}")

    if len(rightSuccessors) == 1:
        rightChild = rightSuccessors.pop()
    elif len(rightSuccessors) > 1:
        raise BrokenPrecondition(
            f"More than one right successor found for vertex {vertex}")
    elif len(rightSuccessors) == 0:
        raise BrokenPrecondition(
            f"No right successor found for vertex {vertex}")

    leftRemainder, rightRemainder = remainder(vertex, left, right)

    return Node(vertex, leftChild, rightChild, leftRemainder, rightRemainder)


class Node():

    def __init__(self, vertex, left, right, leftEdges, rightEdges):
        self.vertex = vertex
        self.left = bort(left, leftEdges, rightEdges)
        self.right = bort(right, leftEdges, rightEdges)

    def show(self):
        return f"({self.left.show()} {self.right.show()})"


class Leaf():

    def __init__(self, leaf):
        self.leaf = leaf

    def show(self):
        return self.leaf


def extract(literal):
    leftParen = literal.index("(")
    rightParen = literal.index(")")
    pairSpan = literal[leftParen + 1:rightParen]
    a, b = pairSpan.split(",")
    a, b = a.strip(), b.strip()
    return a, b


def reachesBack(vertex, edges):
    current = {vertex}
    span = set()
    while current:
        currentEdges = {(a, b) for a, b in edges if a in current}
        current = {b for a, b in currentEdges}
        span |= set(current)
        edges = edges - currentEdges
    return vertex in span


def getTree(model):

    isLeft = lambda s: s[0:5] == 'left('
    isRight = lambda s: s[0:6] == 'right('

    leftCandidates = {literal for literal in model if 'left(' in literal}
    rightCandidates = {literal for literal in model if 'right(' in literal}

    leftEdges = {
        extract(literal)
        for literal in leftCandidates if isLeft(literal)
    }
    rightEdges = {
        extract(literal)
        for literal in rightCandidates if isRight(literal)
    }

    edges = leftEdges | rightEdges
    predecessors = {a for a, _ in edges}
    successors = {b for _, b in edges}
    vertices = predecessors | successors

    roots = {i for i in vertices if i not in successors}
    cycleVertices = [v for v in vertices if reachesBack(v, edges)]

    rooted = len(roots) == 1
    noRoot = len(roots) == 0

    if noRoot:
        raise BrokenPrecondition(f"There is no root")

    if not rooted:
        raise BrokenPrecondition(
            f"{edges} do not specify a tree - more than one root (check nodes {' '.join(roots)})."
        )

    acyclic = len(cycleVertices) == 0

    isTree = acyclic and rooted

    # Lots of heap allocated data structures
    # when all this could be on the stack (or
    # at the very least be discarded when the
    # function returns)

    if isTree:
        root = roots.pop()
        return bort(root, leftEdges, rightEdges)

    elif not acyclic:
        raise BrokenPrecondition(
            f"{edges} do not specify a tree - there are cycles (check nodes {' '.join(cycleVertices)})."
        )
