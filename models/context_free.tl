order n 60 : node.
order t 61 : leaf.
order n 60 : vertex.
order t 61 : vertex.

order i 21 : index.

var a, b : vertex.
var n, m : node.
var t, s : leaf.

var i : index.

var r : rule.

let node.left : dummyvertex.
let node.right : dummyvertex.

let cat : vertex -> category.
let cat : rule -> category.
let leftCat : rule -> category.
let rightCat : rule -> category.

let assign : rule -> node.
let assign : leaf -> token.
let assign : dummyvertex -> vertex.

let left : node -> vertex.
let right : node -> vertex.

let ileft : vertex -> node.
let iright : vertex -> node.

let level : vertex -> index.

-- Constraints on node categories

assign (r, n), cat (r, A), not cat (n, A) -> False.
assign (r, n), leftCat (r, A), not cat (n.left, A) -> False.
assign (r, n), rightCat (r, A), not cat (n.right, A) -> False.

-- Link dummy vertices and vertices

assign (a.left, b), not left (a, b) -> False.
assign (a.right, b), not right (a, b) -> False.

-- Tree behavior

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

left (a, b), level (a, i) -> level(b, i.next).
right (a, b), level (a, i) -> level(b, i.next).
left (a, b), level (b, i.next) -> level(a, i).
right (a, b), level (b, i.next) -> level(a, i).

level (a, i.next) -> not before (a, i).
not before (a, i.next) -> not before (a, i).
level (a, i) -> before (a, i.next).
before (a, i) -> before (a, i.next).

-- Test rules

