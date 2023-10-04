order i 100 : index.
order v 1500 : vertex.

order t 100 : tile.

let vertex.level : level.
let vertex.corner : position.
let vertex.origin : position.

let onvertex : tile -> vertex.

let x : position -> index.
let y : position -> index.

let depth : level -> index.

var a, b : vertex.
var i, j : index.
var t, s : trait.
var p, q : position.
var l, k : level.

-- index order

not before (i, i).
before (i, i.next).
before (i, j) -> before (i, j.next).

-- relation between indices, levels and positions

depth (l, i), before (i, j) -> lowerD (l, j).
depth (k, i), lowerD (l, i) -> before (l, k).

x (p, i), before (i, j) -> lowerX (p, j).
y (p, i), before (i, j) -> lowerY (p, j).

x (p, i), lowerX (q, i) -> beforeX(q, p).
y (p, i), lowerY (q, i) -> beforeY(q, p).

same (p, q), x (p, i) -> x (q, i).
same (p, q), y (p, i) -> y (p, i).

-- map structure

part (a, a) -> False.
part (a, b), before (b.level, a.level) -> False.

part (a, b), beforeX (b.origin, a.origin) -> False.
part (a, b), beforeX (a.corner, b.corner) -> False.
part (a, b), beforeY (b.origin, a.origin) -> False.
part (a, b), beforeY (a.corner, b.corner) -> False.

terminal (a), part (a, b) -> False.

terminal (a) -> same(a.corner, a.origin).

onvertex (t, a), not terminal (a) -> False.

-- trait compatibility

trait (a, t), part (a, b), not compatible (b, t) -> False.

-- here go tile traits and map-specific rules
