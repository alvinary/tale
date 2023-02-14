order i 8 : index.
order q 8 : queen.

var q, r : queen.
var i, j, k, l : index.

let x : queen -> index.
let y : queen -> index.

x (q, i), x (r, i), q != r -> False.
y (q, i), y (r, i), q != r -> False.

diagonalA (i, j, i.next, j.next).
diagonalA (i, j, k, l) -> diagonalA (i, j, k.next, l.next).

diagonal (i, j.next, i.next, j).
diagonalB (i.next, j, k, l.next) -> diagonalB (i, j.next, k.next, l).

x (q, i), y (q, j), x (r, k), y (r, l), diagonalA (i, j, k, l), q != r -> False.
x (q, i), y (q, j), x (r, k), y (r, l), diagonalB (i, j, k, l), q != r -> False.
