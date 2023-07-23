let cat : vertex -> category.
let cat : rule -> category.
let leftCat : rule -> category.
let rightCat : rule -> category.
let assign : rule -> node.
let assign : leaf -> token.
let assign : dummyvertex -> vertex.

var a, b : vertex.
var n, m : node.
var l, f : leaf.
var da, db : dummyvertex.

assign (r, n), cat (r, A), not cat (n, A) -> False.
assign (r, n), leftCat (r, A), not cat (n.left, A) -> False.
assign (r, n), rightCat (r, A), not cat (n.right, A) -> False.
