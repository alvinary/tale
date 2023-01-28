0, 1, 2, 3, 4, 5, 6, 7, 8, 9 : digit.
order n 6 : number.

var i, j : digit.
var d, e, f : digit.
var a, b, c : number.

carry(0, 0, 0).
sum(0, 0, 0).
carry(1, 0, 0).
sum(1, 0, 1).
carry(1, 1, 0).
sum(1, 1, 2).
carry(2, 0, 0).
sum(2, 0, 2).
carry(2, 1, 0).
sum(2, 1, 3).
carry(2, 2, 0).
sum(2, 2, 4).
carry(3, 0, 0).
sum(3, 0, 3).
carry(3, 1, 0).
sum(3, 1, 4).
carry(3, 2, 0).
sum(3, 2, 5).
carry(3, 3, 0).
sum(3, 3, 6).
carry(4, 0, 0).
sum(4, 0, 4).
carry(4, 1, 0).
sum(4, 1, 5).
carry(4, 2, 0).
sum(4, 2, 6).
carry(4, 3, 0).
sum(4, 3, 7).
carry(4, 4, 0).
sum(4, 4, 8).
carry(5, 0, 0).
sum(5, 0, 5).
carry(5, 1, 0).
sum(5, 1, 6).
carry(5, 2, 0).
sum(5, 2, 7).
carry(5, 3, 0).
sum(5, 3, 8).
carry(5, 4, 0).
sum(5, 4, 9).
carry(5, 5, 1).
sum(5, 5, 0).
carry(6, 0, 0).
sum(6, 0, 6).
carry(6, 1, 0).
sum(6, 1, 7).
carry(6, 2, 0).
sum(6, 2, 8).
carry(6, 3, 0).
sum(6, 3, 9).
carry(6, 4, 1).
sum(6, 4, 0).
carry(6, 5, 1).
sum(6, 5, 1).
carry(6, 6, 1).
sum(6, 6, 2).
carry(7, 0, 0).
sum(7, 0, 7).
carry(7, 1, 0).
sum(7, 1, 8).
carry(7, 2, 0).
sum(7, 2, 9).
carry(7, 3, 1).
sum(7, 3, 0).
carry(7, 4, 1).
sum(7, 4, 1).
carry(7, 5, 1).
sum(7, 5, 2).
carry(7, 6, 1).
sum(7, 6, 3).
carry(7, 7, 1).
sum(7, 7, 4).
carry(8, 0, 0).
sum(8, 0, 8).
carry(8, 1, 0).
sum(8, 1, 9).
carry(8, 2, 1).
sum(8, 2, 0).
carry(8, 3, 1).
sum(8, 3, 1).
carry(8, 4, 1).
sum(8, 4, 2).
carry(8, 5, 1).
sum(8, 5, 3).
carry(8, 6, 1).
sum(8, 6, 4).
carry(8, 7, 1).
sum(8, 7, 5).
carry(8, 8, 1).
sum(8, 8, 6).
carry(9, 0, 0).
sum(9, 0, 9).
carry(9, 1, 1).
sum(9, 1, 0).
carry(9, 2, 1).
sum(9, 2, 1).
carry(9, 3, 1).
sum(9, 3, 2).
carry(9, 4, 1).
sum(9, 4, 3).
carry(9, 5, 1).
sum(9, 5, 4).
carry(9, 6, 1).
sum(9, 6, 5).
carry(9, 7, 1).
sum(9, 7, 6).
carry(9, 8, 1).
sum(9, 8, 7).
carry(9, 9, 1).
sum(9, 9, 8).

sum(d, e, f) -> sum (e, d, f).

numsum (a, b, c) <-> leftop (a, c).
numsum (a, b, c) <-> rightop (b, c).

leftop (a, b),
digit (i, a, d) <->
leftopdigit (i, b, d).

leftopdigit (i, a, d),
rightopdigit (i, a, e),
sum (d, e, f) <->
sumdigit (i, a, f).

leftopdigit (i, a, d),
rightopdigit (i, a, e),
carry (d, e, f),
next (i, j) <->
carrydigit (j, a, f).

carrydigit (i, a, d),
sumdigit (i, a, e),
sum (d, e, f) <->
digit (i, a, f).
