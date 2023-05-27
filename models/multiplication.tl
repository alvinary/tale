order i 8 : index.

order o 14 : operation.
order l 15 : literal.

order o 14 : number.
order l 15 : number.

0, 1 : digit.

var i, j, k : index.
var s, p : operation.
var n, m, o : number.
var b : digit.

let bit : number, index -> digit.
let left : operation, index -> digit.
let right : operation, index -> digit.

let first : operation -> number.
let second : operation -> number.

-- Argument binding for sums

sum (s), first (s, n), bit (n, i, b) -> left (s, i, b). -- |operation| |number| |index| |digits| -> large, but with several disjoint number sorts, it should remain small for several separate operations
sum (s), second (s, n), bit (n, i, b) -> right (s, i, b).

-- Shift operation

shift (s), first (s, n), bit (n, i, b) -> bit (s, i.next, b).
shift (s) -> bit (s, i0, 0).
shift (s) -> second (s, s). -- This is so there are less equivalent models (instead of one with second(a, b). another with second(a, c), and so on, you always have second(a, a)

-- Rules for addition

carry (s, i0, 0).

sum(s), left (s, i, 1), right (s, i, 0) -> carry (s, i.next, 0).
sum(s), left (s, i, 0), right (s, i, 0) -> carry (s, i.next, 0).
sum(s), left (s, i, 0), right (s, i, 1) -> carry (s, i.next, 0).
sum(s), left (s, i, 1), right (s, i, 1) -> carry (s, i.next, 1).

sum(s), left (s, i, 0), right (s, i, 0), carry (s, i, 0) -> bit (s, i, 0).
sum(s), left (s, i, 0), right (s, i, 0), carry (s, i, 1) -> bit (s, i, 1).
sum(s), left (s, i, 0), right (s, i, 1), carry (s, i, 0) -> bit (s, i, 1).
sum(s), left (s, i, 0), right (s, i, 1), carry (s, i, 1) -> bit (s, i, 0).
sum(s), left (s, i, 1), right (s, i, 0), carry (s, i, 0) -> bit (s, i, 1).
sum(s), left (s, i, 1), right (s, i, 0), carry (s, i, 1) -> bit (s, i, 0).
sum(s), left (s, i, 1), right (s, i, 1), carry (s, i, 0) -> bit (s, i, 0).
sum(s), left (s, i, 1), right (s, i, 1), carry (s, i, 1) -> bit (s, i, 1).

-- Rules for multiplication

-- mostZero(n), lastZero(n) <-> zero (n).
zero (n) -> digit (n, i, 0). -- Is this ok? 'If' formulas collect both head and body variables, but still, not sure
zero (n), digit (n, i, 1) -> False.

-- mostZero(n), lastOne(n) <-> one (n).
one (n), i != i1 -> digit (n, i, 0).
one (n) -> digit (n, i1, 1).
one (n), i != i1, digit (n, i, 1) -> False.
one (n), digit (n, i1, 0) -> False.

-- inherit the second factor
product (p), not zero (p), second(p, n) -> second(p.next, n).

-- induction on the first factor

-- even case
product (p), not zero (p), first (p, n), even (n) -> product (p.next), first(p.next, n.next), shift (n, n.next). -- woa, makes sense
product (p), not zero (p), first (p, n), even (n) -> sum (p.result), first (p.result, p.next), zeroSecond (p.result). -- zeroSecond(n), second (n, m) -> zero (m). 

-- odd case
product (p), not zero (p), first (p, n), odd (n) -> sum(p.result), first(p.result, p.next).
product (p), not zero (p), second(p, n), odd (n) -> sum(p.result), second(p.result, n).
product (p), not zero (p), first (p, n), odd (n) -> product(p.next), first (p.next, n.next), shiftMost (n, n.next). -- like shift, but with a 'one' least significant digit

-- base case
product (p), first (p, n), one (n) -> base (p).
base (p), second (p, n), bit (n, i, b) -> bit (p.result, i, b).

-- second is zero
product (p), second (p, n), zero (n) -> zero (p.result).

-- first is zero
product (p), first (p, n), zero (n) -> zero (p.result)
