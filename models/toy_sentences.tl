order n 6 : node.
order t 7 : token.

order n 6 : vertex.
order t 7 : vertex.

order i 7 : index.

saw, bought, two, countless, sheep, horses, large, brown : word.

var a, b : vertex.
var n, m : node.
var t, s : token.
var i : index.
var w : word.
var X, Y : category.

let left : node -> vertex.
let right : node -> vertex.

let ileft : vertex -> node.
let iright : vertex -> node.

let level : vertex -> index.
let lex : token -> word.

S, N, V, A, D, NP, VP, NB : category.

cat (brown, A).
cat (large, A).
cat (horses, N).
cat (sheep, N).
cat (countless, D).
cat (two, D).
cat (bought, V).
cat (saw, V).

cat (w, X), lex (t, w) -> cat (t, X).
cat (w, X), lex (t, w), not cat (w, X) -> False.

cat (a, X), cat (a, Y), X != Y -> False.

left (n, a), cat (a, X) -> leftCat (n, X).
right (n, a), cat (a, X) -> rightCat (n, X).

leftCat (n, X), not cat (a, X), left (n, a) -> False.
rightCat (n, X), not cat (a, X), right (n, a) -> False.

rightCat (n, D) -> False.
rightCat (n, A) -> False.
rightCat (n, V) -> False.

leftCat (n, NB) -> False.
leftCat (n, VP) -> False.
leftCat (n, NP), cat (n, X), X != S -> False.
leftCat (n, NB) -> False.
leftCat (n, N) -> False.
leftCat (n, D), cat (n, NB) -> False.
rightCat (n, NP), cat (n, NB) -> False.
leftCat (n, N), cat (n, NB) -> False.
leftCat (n, NB), cat (n, NB) -> False.
leftCat (n, NP), cat (n, NB) -> False.
leftCat (n, NP), cat (n, NP) -> False.
leftCat (n, NB), cat (n, NP) -> False.
leftCat (n, N), cat (n, NP) -> False.

leftCat (n, A), rightCat (n, NB) -> cat (n, NB).
leftCat (n, A), rightCat (n, N) -> cat (n, NB). 
leftCat (n, D), rightCat (n, NB) -> cat (n, NP).
leftCat (n, V), rightCat (n, NP) -> cat (n, VP).
leftCat (n, NP), rightCat (n, VP) -> cat (n, S).
leftCat (n, A) -> cat (n, NB).

not cat (n, VP), leftCat (n, V) -> False.
not cat (n, NP), leftCat (n, D) -> False.

not leftCat (n, D), cat (n, NP) -> False.
not leftCat (n, A), cat (n, NB) -> False.
not rightCat (n, NB), not rightCat (n, N), cat (n, NB) -> False.

cat (n, NB), not rightCat (n, N), not rightCat (n, NB) -> False.
cat (n, NB), leftCat (n, X), X != A -> False.
cat (n, VP), not rightCat (n, NP) -> False.
cat (n, VP), not leftCat (n, V) -> False.
cat (n, NP), not leftCat (n, D) -> False.
cat (n, NP), not rightCat (n, N), not rightCat (n, NB) -> False.
cat (n, S), not rightCat (n, VP) -> False.
cat (n, S), not leftCat (n, NP) -> False.

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

level (n0, i0).
cat (n0, S).

level (a, i.next) -> not before (a, i).
not before (a, i.next) -> not before (a, i).
level (a, i) -> before (a, i.next).
before (a, i) -> before (a, i.next).

before (n, m), right (m, n) -> False.
before (n, m), left (m, n) -> False.
