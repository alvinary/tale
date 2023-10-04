-- Regular Expressions

order regex 20 : Regex.
order s 10 : String.
order i 20 : Index.

a, b : Character.

var R, S, T : Regex.
var s, t, u : String.
var i, j, k : Index.
var char : Character.

is (s, i, j, R.left), is (s, j, k, R.right), concat(R) <-> is (s, j, k, R).
is (s, i, j, R.left), union (R) -> is (s, i, j, R).
is (s, i, j, R.right), union (R) -> is (s, i, j, R).

is (s, i, j, R), union (R),
not is (s, i, j, R.left),
not is (s, i, j, R.right) -> False.

is (s, i, j, R.left),
star (R) -> is (s, i, j, R).

is (s, i, j, R), is (s, j, k, R),
star (R) -> is (s, i, k, R).

symbol (R), char (R), char (s, i, i) -> is (s, i, i, R).

concat (R), union (R) -> False.
symbol (R), concat (R) -> False.
symbol (R), union (R) -> False.
not symbol (R), not concat (R), not union (R) -> False.
