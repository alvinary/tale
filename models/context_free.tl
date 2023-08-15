order n 20 : node.
order t 21 : leaf.
order n 20 : vertex.
order t 21 : vertex.

bool, boolb, num, numb, ifkw, eqkw, cond, eqnum, ubool : category.
r1, r2, r3, r4, r5, r6, r7, r8, r9 : rule.
one, two, three, true, false, nott, eq, and, or : terminal.
if, plus, times, minus, zero : terminal.

order i 21 : index.

var A : category.
var a, b : vertex.
var n, m : node.
var t, s : leaf.
var o : terminal.
var i : index.
var r : rule.

let cat : vertex -> category.
let cat : rule -> category.
let rleftCat : rule -> category.
let rrightCat : rule -> category.
let leftCat : node -> category.
let rightCat : node -> category.

let assign : node -> rule.
let assign : leaf -> terminal.
let assign : dummyvertex -> vertex.

let left : node -> vertex.
let right : node -> vertex.

let ileft : vertex -> node.
let iright : vertex -> node.

let level : vertex -> index.

-- Constraints on node categories

assign (n, r), cat (r, A), not cat (n, A) -> False.
assign (n, r), rleftCat (r, A), not leftCat (n, A) -> False.
assign (n, r), rrightCat (r, A), not rightCat (n, A) -> False.

-- Left cat and right cat

left (n, a), cat (a, A) -> leftCat (n, A).
leftCat (n, A), left (n, a), not cat (a, A) -> False.

right (n, a), cat (a, A) -> rightCat (n, A).
rightCat (n, A), right (n, a), not cat (a, A) -> False.

-- Constraints on leaf categories

terminal (t, o), cat (o, A) -> cat (t, A).
terminal (t, o), cat (t, A), not cat (o, A) -> False.

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

-- Labels of terminals

cat (one, num).
cat (two, num).
cat (true, bool).
cat (false, bool).
cat (three, num).
cat (if, ifkw).
cat (eq, eqkw).
cat (and, bbool).
cat (or, bbool).
cat (plus, bnum).
cat (minus, bnum).
cat (times, bnum).
cat (minus, unum).
cat (nott, ubool).
cat (zero, num).

-- List of terminals:
-- one, two, three, false, true, if, eq, and,
-- or, plus, minus, times, nott

-- Rules

cat (r1, bool).
leftCat (r1, bool).
rightCat (r1, boolb).

cat (r2, boolb).
leftCat (r2, boolop).
rightCat (r2, bool).

cat (r3, num).
leftCat (r3, num).
rightCat (r3, numb).

cat (r4, numb).
leftCat (r4, numop).
rightCat (r4, num).

cat (r5, num).
leftCat (r5, ifkw).
rightCat (r5, cond).

cat (r6, cond).
leftCat (r6, bool).
rightCat (r6, num).

cat (r7, bool).
leftCat (r7, num).
rightCat (r7, eqnum).

cat (r8, eqnum).
leftCat (r8, eqkw).
rightCat (r8, num).

cat (r9, bool).
leftCat (r9, ubool).
rightCat (r8, bool).

