
let type.left : dtype.
let type.right : dtype.

let assign : dtype -> type.

match (t, s) -> match (s, t).

-- Base case
simple (t), simple (s), cat (t, x), cat (s, x) -> match (t, s).

-- Recursive case
compound (t), compound (s), matchLeft (t, s), matchRight (t, s) -> match(t, s).

-- Add the relevant '-> False' cases for both.

match (t.left, s) -> matchLeft (t, s).

assign ()
