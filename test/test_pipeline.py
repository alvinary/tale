from tale.pipeline import *

program = '''
shore, docks : place.
cabbage, goat, wolf, farmer : actor.
order i 6 : index.

let at : index, actor -> place.
let ferry : index, player -> actor.

var p : place.
var a, b, c : actor.
var i : index.

let docks.opposite = shore.
let shore.opposite = docks.

at(i, a, p), at (i, b, p), not at (i, farmer, p), eats (a, b) -> False.
at(i, a, p), ferry(i, farmer, a) -> at(i.next, a, p.opposite).

at (i0, farmer, shore).
at (i0, wolf, shore).
at (i0, cabbage, shore).
at (i0, goat, shore).

'''

def test_pipeline():
    count = 10
    for model in pipeline(program):
        print(model)
        print("")
        count -= 1
        if count == 0:
            break
    assert False
