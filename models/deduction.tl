order p 25 : proof.
order v 80 : formula.
order h 14 : hypothesis.

let proof.1 : dummyformula.
let proof.2 : dummyformula.
let proof.3 : dummyformula.
let proof.formula : dummyformula.

let formula.left : dummyformula.
let formula.right : dummyformula.
let formula.term : dummyformula.

let hypothesis.formula : dummyformula.

let assign : dummyformula -> formula.

var p, q : proof.
var h : hypothesis.
var a : atom.

-- match ------------------------------------------------------------------------

-- use digits to prevent 'cubic' explosion

match (p, q) -> match (q, p).

match(p, q.left) -> matchL (p, q).
match(p, q.right) -> matchR (p, q).

not match(p, q.left), matchL (p, q) -> False.
not match(p, q.right), matchR (p, q) -> False.

-- when binary formulas match

match (p, q), binary (p), not binary (q) -> False.

match (p, q), binary (p) -> matchL (p.left, q).
match (p, q), binary (p) -> matchR (p.right, q).
match (p, q), binary (p), not matchL (p, q) -> False.
match (p, q), binary (p), not matchR (p, q) -> False.

match (p, q), binary (p), not matchL (p, q) -> False.
match (p, q), binary (p), not matchR (p, q) -> False.

-- when unary formulas match

match (p, q), unary (p) -> match (p.term, q.term).
match (p, q), unary (p) -> matchOperator (p, q).

-- when leaves match

match (f, g), leaf (f) -> symbol (f, a), symbol (g, a).
match (f, g), leaf (f), not symbol (f, a), symbol (g, a) -> False.
match (f, g), leaf (f), symbol (f, a), not symbol (g, a) -> False.

-- toDo: check possibly shorter alternative: match (p, q) -> sameFormula (p, q)

-- connectives ------------------------------------------------------------------

-- -- imply

implyI (p), hypothesis (p, h) -> cancel (p, h).
implyI (p), hypothesis (p, h) -> matchL (h.formula, p.formula).
implyI (p), hypothesis (p, h) -> matchR (p.1, p.formula).

implyE (p) -> matchR (p.formula, p.2).
implyE (p) -> matchL (p.1, p.2).

-- -- auxiliary

-- -- and

andI (p) -> matchL (p.1, p.formula).
andI (p) -> matchR (p.2, p.formula).

andEL (p) -> match (p.formula, p.1).
andER (p) -> match (p.formula, p.2).

-- -- or

-- orIL (p)
-- orIR (p)
-- orE (p)

-- -- not

-- -- RAA, bottom, top

-- valid use of hypothesis -----------------------------------------------------

assumption (p), hypothesis (p, h) -> assign (h.formula, p.formula).
hypothesis (p, h), proves (p, q), not cancel (q, h) -> hypothesis (q, h).
hypothesis (p, h), root (p) -> False.

-- correct proofs --------------------------------------------------------------

proves (p.1, p.formula), proves (p, q) -> proves (p.1, r).
proves (p.2, p), proves (p, q) -> proves (p.2, r).
proves (p.3, p), proves (p, q) -> proves (p.3, r).
