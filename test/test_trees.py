from tale.pipeline import *
from tale.objects import *

MODELS = 10

program = '''
order n 10 : node.
order t 11 : token.

order n 10 : vertex.
order t 11 : vertex.

order i 11 : index.

var a, b : vertex.
var n, m : node.
var t, s : token.
var i : index.

let left : node -> vertex.
let right : node -> vertex.

let ileft : vertex -> node.
let iright : vertex -> node.

let level : vertex -> index.

left (a, a) -> False.
right (a, a) -> False.

right (t, a) -> False.
left (t, a) -> False.

left (n, a) -> ileft (a, n).
right (n, a) -> iright (a, n). 

left (a, b), right (a, b) -> False.

right (n, a) -> isRight (a).
left (n, a) -> isLeft (a).

isLeft (a), isRight (a) -> False.

left (a, b), level (a, i) -> level(b, i.next).
right (a, b), level (a, i) -> level(b, i.next).
left (a, b), level (b, i.next) -> level(a, i).
right (a, b), level (b, i.next) -> level(a, i).

level (n1, i1).

level (a, i.next) -> not before (a, i).
not before (a, i.next) -> not before (a, i).
level (a, i) -> before (a, i.next).
before (a, i) -> before (a, i.next).
'''


def test_trees():
    models = pipeline(program)

    if not models:
        print("Instance is not satisfiable")
        assert False

    for index, model in zip(range(MODELS), models):
        tree = getTree(model)
        print(tree.show(), '\n')
