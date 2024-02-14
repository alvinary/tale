order i 30 : index.
order v 130 : vertex.

let vertex.ox : ox.
let vertex.oy : oy.
let vertex.cx : cx.
let vertex.cy : cy.

let at : ox -> index.
let at : oy -> index.
let at : cx -> index.
let at : cy -> index.

var a, b : vertex.
var i, j : index.

var ox1, ox2 : ox.
var oy1, oy2 : oy.
var cx1, cx2 : cx.
var cy1, cy2 : cy.

-- O (v**2)

before (a, a.next).
before (a, b) -> before (a, b.next).

-- O (v**2)

part (a, b), before (b, a) -> False.

-- O (i ** 2)

before (i, i.next).
before (i, j) -> before (i, j.next).

-- O (v * i)

tile (a), at (a.ox, i) -> at (a.oy, i), at (a.cx, i), at (a.cy, i).

-- O (v*v)

part (a, b) -> within (b, a).

-- O (v*v)

within (b, a), before(a.cy, b.cy) -> False.
within (b, a), before(a.cx, b.cx) -> False.
within (b, a), before(b.oy, a.oy) -> False.
within (b, a), before(b.ox, a.ox) -> False.

-- O(4*v*i)

at (a.cx, i) -> before (a.cx, i.next).
before (a.cx, i) -> before (a.cx, i.next).
at (a.cy, i) -> before (a.cy, i.next).
before (a.cy, i) -> before (a.cy, i.next).
at (a.ox, i) -> before (a.ox, i.next).
before (a.ox, i) -> before (a.ox, i.next).
at (a.oy, i) -> before (a.oy, i.next).
before (a.oy, i) -> before (a.oy, i.next).

-- Showing part and at, 1 model, power saver mode, low battery
-- v = 20, i = 40 : 6s
-- v = 40, i = 40 : 9s
-- v = 60, i = 40 : 12s
-- v = 80, i = 40 : 19s
-- v = 100, i = 40 : 24s
-- v = 120, i = 40 : 39s
-- v = 140, i = 40 : 51s  (45s en 30x30)

-- O (v * v)

terminal (a), not tile (a) -> False.
terminal (a), part (a, b) -> False.
tile (a), not terminal (a) -> False.

-- O ()

-- limitar la cantidad de partes
-- f : v x v -> {1, ..., i, ... max}
-- part (a, b), not f (a, b, 1), ...,  not f (a, b, i), ..., not f (a, b, max) -> False.
