from tale.pipeline import *

MODELS = 10

program = '''
order token 5 : token.
order node 4 : node.
order node 4 : vertex.
order token 5 : vertex.
order lv 5 : level.

let left : node -> vertex.
let right : node -> vertex.
let parent : vertex -> node.
let level : node -> level.

var t, s : node.
var a, b : vertex. 
var n, m : level.

not left (t, t).
not right (t, t).
left (t, a) -> not right (t, a).
right (t, a) -> not left (t, a).

left (t, a) -> parent (a, t).
right (t, a) -> parent (a, t).

left (t, s) -> not left (s, t).
right (t, s) -> not right (s, t).

level (t, n), right (t, s) -> level (s, n.next).
level (t, n), left (t, s) -> level (s, n.next).

level (t, lv0) -> parent (t, t).
level (node0, lv0).

before (n, n.next).
before (n, m) -> before (n, m.next).
not before (n, n).
before (n, m) -> not before (m, n).
'''


def test_pipeline():
    for index, model in zip(range(MODELS), pipeline(program)):
        for a in sorted(list(model)):
            print(a)
        print("")
    assert False
