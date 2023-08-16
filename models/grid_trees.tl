let dLeft : tree -> tree.
let rRight : tree -> tree.
let left : tree -> tree.
let right : tree -> tree.

var a, b : tree.

-- tree nodes are virtual or real

not virtual (a), not real (a) -> False.
not leaf (a), not node (a) -> False.

virtual (a), real (a) -> False.
leaf (a), node (a) -> False.

-- only real nodes are branches of each other

left (a, b), not real (a) -> False.
left (a, b), not real (b) -> False.

right (a, b), not real (a) -> False.
right (a, b), not real (b) -> False.

-- virtual nodes are either left branching or right branching

real (a), lefter (a) -> False.
real (a), righter (a) -> False.
virtual (a), righter (a), lefter (a) -> False.

-- virtual nodes 'propagate' branches back in the tree,
-- eventually reaching a real node

virtual (a), lefter (a.left) -> lefter (a).
real (a.left), lefter (a) -> dLeft (a, a.left).
dLeft (a.left, b) -> dLeft (a, b).
real (a), dLeft (a, b) -> left (a, b).

virtual (a), righter (a.right) -> righter (a).
righter (a), real (a.right) -> dRight(a, a.right).
dRight (a.right, b) -> dRight (a, b).
real (a), dRight (a, b) -> right (a, b).

-- virtual nodes can only have real nodes as branches

dRight (a, b), not real (b) -> False.
dLeft (a, b), not real (b) -> False.

-- 'regular' tree constraints

left (a, b), real (b), real (a), a.left != b -> False.
right (a, b), real (b), real (a), a.right != b -> False.
