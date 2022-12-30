order n 9 : node.
order t 10 : token.

order n 9 : vertex.
order t 10 : vertex.

var a, b, c : vertex.
var l, v, f : level.
var t, s, q : node.

left (a, b) -> below(a, b).
right (a, b) -> below(a, b).

below (a, a).
below (a, b), below (b, c) -> below (a, b).
below (a, b), below (b, a), a != b -> False.

rightOf (a, a).
left (a, b) -> rightOf (a, b).
right (a, b) -> rightOf (b, a).
rightOf (a, b), rightOf (b, c) -> rightOf (a, c).
rightOf (a, b), rightOf (b, a), a != b -> False.

left (q, a) -> False.
right (q, a) -> False.
