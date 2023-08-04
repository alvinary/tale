order c 4 : color.
order v 10 : vertex.

let color : vertex -> color.

var a, b : vertex.
var c : color.

-- Get planar graphs / graphs with 4 colors
edge (a, b), color (a, c), color (b, c) -> False.
