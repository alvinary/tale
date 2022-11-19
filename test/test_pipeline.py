from tale.pipeline import *

program = '''
shore, docks : place.
cabbage, goat, wolf, farmer : actor.
cabbage, goat, wolf : factor.
order i 8 : index.

let at : index, actor -> place.
let ferry : index -> factor.

var p : place.
var a, b : actor.
var c : factor.
var i : index.

let docks.opposite = shore.
let shore.opposite = docks.

at (i, a,  p), at (i, b, p), eats (a, b) -> ate (i, a, b).
at(i, a, p), at (i, b, p), not at (i, farmer, p), eats (a, b) -> False.

ferry (i, c), at (i, farmer, p), not at (i, c, p) -> False.
ferry (i, c), at (i, c, p) -> at (i.next, c, p.opposite).
ferry (i, c), at (i, c, p) -> at (i.next, farmer, p.opposite).

not ferry (i, c), at (i, c, p) -> at (i.next, c, p).

eats (goat, cabbage).
eats (wolf, goat).

at (i0, farmer, shore).
at (i0, wolf, shore).
at (i0, cabbage, shore).
at (i0, goat, shore).

not at (i7, cabbage, docks) -> False.
not at (i7, goat, docks) -> False.

at (i, cabbage, docks), at (i, goat, docks) -> won(i, farmer).
won (i, farmer) -> won (i.next, farmer).

'''

def test_pipeline():
    count = 10
    for model in pipeline(program):
        for a in sorted(list(model)):
            print(a)
        print("")
        count -= 1
        if count == 0:
            break
    assert False
