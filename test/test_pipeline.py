from tale.pipeline import *

MODELS = 10

program = '''

-- Define the relevant sorts

shore, docks : place.
cabbage, goat, wolf, farmer : actor.
cabbage, goat, wolf : factor.
order i 8 : index.

-- Each actor is at exactly one place
-- at any given time

let at : index, actor -> place.

-- Define variables

var p : place.
var a, b : actor.
var c : factor.
var i : index.

-- The docks are opposite from the shore,
-- and viceversa

let docks.opposite = shore.
let shore.opposite = docks.

-- If an actor eats another, and they are
-- in the same place, they will invariably
-- eat it.

ate (i, a, b), not eats (a, b) -> False.
at (i, a,  p), at (i, b, p), eats (a, b), not at (i, farmer, p) <-> ate (i, a, b).

-- We don´t want models where the farmer
-- was not keeping watch and someone wound up getting eaten.

at(i, a, p), at (i, b, p), not at (i, farmer, p), eats (a, b) -> False.


-- These are the rules for ferrying:
-- * The farmer can't ferry the wolf from one place to another
-- * The farmer cannot ferry the cabbage and the goat at the same time
-- (otherwise they can just take both to the docks on the first turn
-- and be done)
-- * The farmer can't ferry you from place A to B starting at place B.
-- * If you are transported by ferry at time t, you'll be at the opposite part
-- of the river on t + 1 
-- * The farmer drives the ferry, and cannot just send you off from A to B
-- and stay at A.
-- * Anything that's not ferried stays where it is

ferry (i, wolf) -> False.
ferry (i, a), ferry (i, b), a != b -> False.
ferry (i, c), at (i, farmer, p), not at (i, c, p) -> False.
ferry (i, c), at (i, c, p) -> at (i.next, c, p.opposite).
ferry (i, c), at (i, c, p) -> at (i.next, farmer, p.opposite).
not ferry (i, c), at (i, c, p) -> at (i.next, c, p).

-- Who eats whom

eats (goat, cabbage).
eats (wolf, goat).
not eats (a, a).
not eats (farmer, a).
not eats (cabbage, a).
not eats (goat, wolf).
not eats (a, farmer).

-- Initial state

at (i0, farmer, shore).
at (i0, wolf, shore).
at (i0, cabbage, shore).
at (i0, goat, shore).

-- The farmer stops ferrying when he wins
won (i, farmer), ferry (i, c) -> False.

-- Characterization of a bad ending and a good ending
not at (i7, cabbage, docks) -> False.
not at (i7, goat, docks) -> False.
at (i, cabbage, docks), at (i, goat, docks) -> won(i, farmer).
not at (i, cabbage, docks), not at (i, goat, docks), won (i, farmer) -> False.

won (i, farmer) -> won (i.next, farmer).
won (i, farmer), ferry (i, a) -> False.
'''


def test_pipeline():
    for index, model in zip(range(MODELS), pipeline(program)):
        for a in sorted(list(model)):
            print(a)
        print("")
