from tale.pipeline import *
from tale.objects import *

MODELS = 10

program = '''
order n 9 : node.
order t 10 : token.

order n 9 : vertex.
order t 10 : vertex.

var a, b, c : vertex.
var n, m, o : node.
var t, s, w : token.

let left : node -> vertex.
let right : node -> vertex.

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

'''

def test_trees():
    models = pipeline(program)
    
    if not models:
        print("Instance is not satisfiable")
        assert False
    
    for index, model in zip(range(MODELS), models):
        try:
            tree = getTree(model)
            print(tree.show(), '\n')
        except BrokenPrecondition:
            assert False

