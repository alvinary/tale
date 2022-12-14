from tale.pipeline import *
from tale.objects import *

MODELS = 10

program = '''

order n 9 : node.
order t 10 : token.

order n 9 : vertex.
order t 10 : vertex.

order s 6 : symbol.
order r 15 : rule.

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

def test_grammars():

    models = pipeline(program)
    trees = set()
    
    if not models:
        print("Instance is not satisfiable")
        assert False
    
    for model in models:
        try:
            tree = getTree(model)
            trees.add(tree.show())
            if len(trees) > MODELS:
                break
        except BrokenPrecondition:
            assert False

    print("\n\n".join(trees))

    assert False
            
