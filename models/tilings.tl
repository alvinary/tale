-- dramatis personae

order i 40 : index.
order n 400 : node.
order t 1600 : tile.

-- terrain constants should be specified programatically
-- grass, shallowWater, ... : terrain.

-- dry, moist, blocked, free, beachy, greeny, browny, sandy, ... : property

-- function types

let tile.x : index.
let tile.y : index.

let node.upper : index.
let node.lower : index.
let node.left : index.
let node.right : index.

let tile.t : terrain.

-- variables

var i, j : index.
var a, b : node.
var t : tile.
var p : property.

-- 'before' for nodes and indices
-- this should be unfolded into <= for all order sorts, don't you agree?

before (a, a.next).
before (a, b) -> before (a, b.next).

before (i, i.next).
before (i, j) -> before (i, i.next).

-- DAG rules

part (a, b), before (b, a) -> False.

-- constraints on part positions

part (a, b) -> b.right <= a.right.
part (a, b) -> b.upper <= a.upper.
part (a, b) -> a.lower <= b.lower.
part (a, b) -> a.left <= a.left.

-- constraints on tile positions

part (a, t), t.x <= a.right -> False.
part (a, t), t.y <= a.upper -> False.
part (a, t), a.lower <= t.y -> False.
part (a, t), a.left <= t.x -> False.

-- terrain rules


