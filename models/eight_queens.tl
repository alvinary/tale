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

diagonalB (i.next, j, i, j.next).
diagonalB (i, j, k.next, l) -> diagonalB (i, j, k, l.next).

x (q, i), y (q, j), x (r, k), y (r, l), diagonalA (i, j, k, l), q != r -> False.
x (q, i), y (q, j), x (r, k), y (r, l), diagonalB (i, j, k, l), q != r -> False.
