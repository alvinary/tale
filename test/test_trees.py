from tale.pipeline import *

MODELS = 10

program = '''
order token 5 : token.
order node 4 : node.
order token 5 : vertex.
order node 4 : vertex.
order lv 5 : level.

let left : node -> vertex.
let right : node -> vertex.
let parent : vertex -> node.
let level : node -> level.

var t, s : node.
var a, b : vertex. 
var n : level.

left (t, t) -> False.
right (t, t) -> False.
left (t, a), right (t, a) -> False.
left (t, a) -> parent (a, t).
right (t, a) -> parent (a, t).

level (t, n), right (t, s) -> level (s, n.next).
level (t, lv0) -> parent (t, t).
'''

def test_pipeline():
    for index, model in zip(range(MODELS), pipeline(program)):
        for a in sorted(list(model)):
            print(a)
        print("")
    assert False
