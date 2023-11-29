NEWLINE = "\n"


def remainder(vertex, left, right):
    left = {(a, b) for a, b in left if a != vertex}
    right = {(a, b) for a, b in right if a != vertex}
    return left, right


def successors(vertex, relation):
    successors = {b for a, b in relation if a == vertex and b != vertex}
    return successors


def bort(vertex, left, right):

    leftSuccessors = successors(vertex, left)
    rightSuccessors = successors(vertex, right)
    
    if len(leftSuccessors) == 0 and len(rightSuccessors) == 0:
        return Leaf(vertex)
        
    if len(leftSuccessors) == 1 and len(rightSuccessors) == 1:
        leftChild = leftSuccessors.pop()
        rightChild = rightSuccessors.pop()
        leftRemainder, rightRemainder = remainder(vertex, left, right)
        return Node(vertex, leftChild, rightChild, leftRemainder, rightRemainder)
        
    else:
        error_message = '\nThere is an unexpected number of left and right nodes!'
        error_message = error_message + f'\nWhat I see is\nleft: { " ".join(leftSuccessors)}\nright: {" ".join(rightSuccessors)}'
        raise Exception(error_message)


class Node():

    def __init__(self, vertex, left, right, leftEdges, rightEdges):
        self.vertex = vertex
        self.left = bort(left, leftEdges, rightEdges)
        self.right = bort(right, leftEdges, rightEdges)

    def show(self):
        return f"({self.left.show()} {self.right.show()})"
        
    def replace(self, a, b):
        self.left.replace(a, b)
        self.right.replace(a, b)


class Leaf():

    def __init__(self, leaf):
        self.leaf = leaf

    def show(self):
        return self.leaf
        
    def replace(self, a, b):
        if self.leaf == a:
            self.leaf = b


def extract(literal):
    leftParen = literal.index("(")
    rightParen = literal.index(")")
    argumentsSpan = literal[leftParen + 1:rightParen]
    arguments = argumentsSpan.split(",")
    if len(arguments) == 2:
        a, b = arguments[0].strip(), arguments[1].strip()
        return a, b
    else:
        return arguments


def reachesBack(vertex, edges):
    current = {vertex}
    span = set()
    while current:
        currentEdges = {(a, b) for a, b in edges if a in current}
        current = {b for a, b in currentEdges}
        span |= set(current)
        edges = edges - currentEdges
    return vertex in span


def getTree(model, test=False):

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
    
    if test:
        rooted = len(roots) == 1
        cycles = [v for v in vertices if reachesBack(v, edges)]
        
        if not rooted:
            raise Exception(
                f"More than one root found (roots are {', '.join(roots)})")
                
        if cycles:
            raise Exception(
                f"There are loops connecting some vertices to themselves ({', '.join(cycles)})")
        

    # Lots of heap allocated data structures
    # when all this could be on the stack (or
    # at the very least be discarded when the
    # function returns)

    root = roots.pop()
    
    return bort(root, leftEdges, rightEdges)


def stringSpecification(name, sequence):
    facts = []
    characters = set()
    for index, char in enumerate(sequence):
        facts.append(f'{char} ({name}, {index}, {index}).')
    return name, facts, characters


def makeStrings(strings):
    allNames, allFacts, allCharacters = [], [], set()
    for index, string in enumerate(strings):
        name = '{STRING_PREFIX}{index}'
        name, facts, characters = stringSpecification(string)
        allNames.append(name)
        allFacts += facts
        allCharacters |= characters
    return allNames, allFacts, allCharacters
    
    
def getSentence(model):

    isLeft = lambda s: s[0:5] == 'left('
    isRight = lambda s: s[0:6] == 'right('
    isLex = lambda s: s[0:4] == 'terminal('
    isRoot = lambda s: s[0:5] == 'root('

    leftCandidates = {literal for literal in model if 'left(' in literal}
    rightCandidates = {literal for literal in model if 'right(' in literal}
    lexCandidates = {literal for literal in model if 'terminal(' in literal and 'not terminal' not in literal}
    rootCandidates = {literal for literal in model if 'root(' in literal and 'not root' not in literal}
    
    print(lexCandidates)

    leftEdges = {
        extract(literal)
        for literal in leftCandidates if isLeft(literal)
    }
    rightEdges = {
        extract(literal)
        for literal in rightCandidates if isRight(literal)
    }
    lexicalItems = {
        extract(literal)
        for literal in lexCandidates
    }
    roots = {
        extract(literal).pop()
        for literal in rootCandidates
    }
    
    print(lexicalItems)

    edges = leftEdges | rightEdges
    predecessors = {a for a, _ in edges}
    successors = {b for _, b in edges}
    vertices = predecessors | successors
    
    edges = leftEdges | rightEdges
    predecessors = {a for a, _ in edges}
    successors = {b for _, b in edges}
    vertices = predecessors | successors

    root = roots.pop()
    
    tree = bort(root, leftEdges, rightEdges)
    
    for a, b in lexicalItems:
        tree.replace(a, b)
        
    return tree
