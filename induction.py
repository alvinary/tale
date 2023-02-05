from tale.pipeline import *
from tale.objects import *

# Here we set a different recursion limit

# This is done because tatsu is very functional,
# CPython does not apply tail recursion optimizations,
# And this same program gets a maximum recursion depth
# exceeded when using the full grammar, but not when
# cutting it to half its size (so it's not an issue
# with tatsu or the grammar - it's just Python is not
# Haskell and this is not the intended use)

# TODO: check if pypy behaves the same
# TODO: change recursive list rules to blah*
# ('regular-grammar style') rules

import sys
sys.setrecursionlimit(1500)

MODELS = 5

program = '''

order n 6 : node.
order t 7 : token.

order n 6 : vertex.
order t 7 : vertex.

order s 10 : symbol.
order r 10 : rule.

var a, b, c : vertex.
var n, m, o : node.
var t, s, w : token.
var A, B, C : symbol.

let left : node -> vertex.
let right : node -> vertex.

let assign : node -> rule.

left (a, a) -> False.
right (a, a) -> False.

left (t, a) -> False.
right (t, a) -> False.

left (a, b), right (a, b) -> False.

left (a, b), right (c, b) -> False.
left (a, b), left (c, b), a != c -> False.
right (a, b), right (c, b), a != c -> False.

left (a, b) -> below (a, b).
right (a, b) -> below (a, b).

left (a, b) -> above (b, a).
right (a, b) -> above (b, a).

below (a, b), below (b, c) -> below (a, c).
below (a, a) -> False.
below (a, b), below (b, a) -> False.

below (a, n0) -> False.
not below (n0, a), a != n0 -> False.

left (a, b), left (a, c), b != c -> False.
right (a, b), right (a, c), b != c -> False.

not below (n0, a), a != n0 -> False.
not above (a, n0), a != n0 -> False.

below (a, b) -> above (b, a).
above (a, b), above (b, c) -> above (a, c).
above (a, b), above (b, a) -> False.
above (a, a) -> False.

left (a, b) -> rightOf (b, a).
right (a, b) -> rightOf (a, b).
rightOf (a, b), rightOf (b, c) -> rightOf (a, c).
rightOf (a, b), rightOf (b, a) -> False.
rightOf (a, a) -> False.

before (n, n) -> False.
before (n, n.next).
before (n, m), before (m, o) -> before (n, o).
before (n, m), before (m, n) -> False.

before (t, t) -> False.
before (t, t.next).
before (t, s), before (s, w) -> before (t, w).
before (t, s), before (s, t) -> False.

rightOf (t, s), before (s, t) -> False.
rightOf (n, m), before (m, n) -> False.

leftSymbol (r, B), assign (n, r) <-> leftSymbol (n, B).
rightSymbol (r, C), assign (n, r) <-> rightSymbol (n, C).
symbol (r, A), assign (n, r) <-> symbol (n, A).

left (n, a), leftSymbol (n, B), not symbol (a, B) -> False.
right (n, a), rightSymbol (n, C), not symbol (a, C) -> False.

symbol (n, A), symbol (n, B), A != B -> False.
symbol (t, A), symbol (t, B), A != B -> False.
'''

def decode(model):
    objects = []
    return objects

def encode(structure, tag):
    facts = []
    return facts

# TODO: handle branching and unsatisfiable cores
def induce(baseTheory, positive, negative, step=DEFAULT_STEP):
    
    currentTheory = baseTheory
    samples = []
    
    while not stop:

        extend(currentTheory, positive, negative)
        
        for i in range(step):
            results = models(currentTheory)
            newSamples = [decode(model) for model in results]
            newSamples = *samples
            samples += newSamples

        for sample in newSamples:
            newPositive, newNegative = tag(sample)
            positive += newPositive
            negative += newNegative
    
        stop = ask()

    return currentTheory, samples
