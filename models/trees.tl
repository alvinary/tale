order n 6 : node.
order t 7 : token.

order n 6 : vertex.
order t 7 : vertex.

order i 8 : index.

var a, b, c : vertex.
var n, m, o : node.
var t, s, w : token.
var i, j : index.

let left : node -> vertex.
let right : node -> vertex.

let ileft : vertex -> node.
let iright : vertex -> node.

let level : vertex -> index.

left (a, a) -> False.
right (a, a) -> False.

right (t, a) -> False.
left (t, a) -> False.

left (n, a) -> ileft (a, n).
right (n, a) -> iright (a, n). 

left (a, b), right (a, b) -> False.

right (n, a) -> isRight (a).
left (n, a) -> isLeft (a).

isLeft (a), isRight (a) -> False.

left (n, a), level (n, i) -> level(a, i.next).
right (n, a), level (n, i) -> level(a, i.next).

level (n0, i0).