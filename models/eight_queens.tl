order i 8 : index.
order q 8 : queen.

var q, r : queen.
var i, j, k, l : index.

at (q, i, k), at (r, i, j), q != r -> False.
at (q, k, i), at (r, j, i), q != r -> False.

diagonal (q, r) -> False.

diagonal (i, j, i.next, j.next).
diagonal (i, j, k, l) -> diagonal (i, j, k.next, l.next).
diagonal (i, j, k, l) -> diagonal (k, l, i, j).

at (q, i, j), at (r, k, l), diagonal (i, j, k, l), r != q -> False.

diagonal (i, j, k, l) -> not diagonal (i, j, k.next, l).
diagonal (i, j, k, l) -> not diagonal (i, j, k, l.next).
not diagonal (i, j, k, l) -> not diagonal (k, l, i, j).
