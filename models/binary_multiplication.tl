1, 0 : digit.

order i 8 : index.

order n 8 : operand.
order u 8 : unary.
order o 7 : operation.

order n 8 : number.
order o 7 : number.
order u 8 : number.

var d, e : digit.
var i, j, k : index.

var n, m : operand.
var p, q, s, t : operation.

let bit : number, index -> digit. 

let left : operand -> number.
let right : operand -> number.

-- a * b = b                   (if a = 1)
-- a * b = b + shift(k * b)    (if a = 2k + 1)
-- a * b = shift(k * b)        (if a = 2k)


-- shift(u) =>
--   u.digits[i] = u.argument.digits[i-1]
--   u.digits[1] = 0

-- mult(p), p.right != 0 =>
--   sum(p.result)
--   right(p.result, p.right)
--   left(p.result, p.)
