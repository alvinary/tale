let left : tree -> tree.
let right : tree -> tree.
let dDir : tree -> tree.

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

-- virtual nodes are either left branching or right branching. Real nodes are both.

real (a) -> lefter(a), righter (a).
virtual (a), righter (a), lefter (a) -> False.

-- virtual nodes 'propagate' branches back in the tree,
-- eventually reaching a real node

dLeft (a, b) -> dDir (a, b).
dRight (a, b) -> dDir (a, b).

virtual (a), lefter (a) -> dLeft (a, a.left).
dLeft (a.left, b), virtual (a) -> dLeft (a, b).
real (a), dLeft (a.left, b) -> left (a, b).

virtual (a), righter (a) -> dRight (a, a.right).
dRight (a.right, b), virtual (a) -> dRight (a, b).
real (a), dRight (a.right, b) -> right (a, b).

-- virtual nodes can only have real nodes as branches

dRight (a, b), not real (b) -> False.
dLeft (a, b), not real (b) -> False.

-- 'regular' tree constraints

left (a, a) -> False.
right (a, a) -> False.

left (a, b), before (b, a) -> False.
right (a, b), before (b, a) -> False.

before (a, a).
before (a, a.left).
before (a, a.right).
before (a, b) -> before (a, b.left).
before (a, b) -> before (a, b.right).
