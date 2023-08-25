leaf, virtual, real : class.

let branch : nonroot -> tree.
let class : tree -> class.

var a, b : tree.

class (a, leaf) -> leaf (a).
class (a, real) -> real (a).
class (a, virtual) -> virtual (a).

virtual (a), real (a) -> False.
virtual (a), leaf (a) -> False.
real (a), leaf (a) -> False.

leaf (a), vl (a) -> False.
leaf (a), vr (a) -> False.

right (a, b), leaf (a) -> False.
left (a, b), leaf (a) -> False.

right (a, b), virtual (a) -> False.
left (a, b), virtual (a) -> False.

right (a, b), virtual (b) -> False.
left (a, b), virtual (b) -> False.

carryLeft (a, b), real (a) -> False.
carryRight (a, b), real (a) -> False.

vl (a) -> virtual (a).
vr (a) -> virtual (a).
vl (a), vr (a) -> False.
virtual (a), not vl (a), not vr (a) -> False.

vl (a.left), virtual (a) -> vl (a).
vr (a.right), virtual (a) -> vr (a).
vl (a), virtual (a.left) -> vl (a.left).
vr (a), virtual (a.right) -> vr (a.right).

vl (a), real (a.left) -> carryLeft (a, a.left).
vl (a), leaf (a.left) -> carryLeft (a, a.left).
vl (a), carryLeft (a.left, b) -> carryLeft (a, b).

carryLeft (a, b), not vl (a) -> False.
carryRight (a, b), not vr (a) -> False.

vr (a), real (a.right) -> carryRight (a, a.right).
vr (a), leaf (a.right) -> carryRight (a, a.right).
vr (a), carryRight (a.right, b) -> carryRight (a, b).

carryLeft (a, b), real (a) -> False.
carryRight (a, b), real (a) -> False.

carryLeft (a.left, b), real (a) -> left (a, b).
carryRight (a.right, b), real (a) -> right (a, b).

real (a), real (a.left) -> left (a, a.left).
real (a), real (a.right) -> right (a, a.right).

real (a), leaf (a.left) -> left (a, a.left).
real (a), leaf (a.right) -> right (a, a.right).

left (a, b) -> branch (b, a).
right (a, b) -> branch (b, a).
vl (a.left) -> branch (a.left, a).
vr (a.right) -> branch (a.right, a).
