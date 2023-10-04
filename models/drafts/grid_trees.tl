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

not beforeLeft (a, a).
not beforeLeft (a, a.right).
not beforeLeft (a, b) -> not beforeLeft (a, b.right).
not beforeLeft (a, b.right) -> not beforeLeft (a, b).

not afterLeft (a, a).
not afterLeft (a, a.right).
not afterLeft (a, b) -> not afterLeft (a, b.right).
not afterLeft (a, b.right) -> not afterLeft (a, b).

beforeLeft (a, a.left).
beforeLeft (a, b) -> beforeLeft (a, b.left).
beforeLeft (a, b) -> not beforeLeft (b, a).
beforeLeft (a, b) -> beforeLeft (a, a.right).

afterLeft (a.left, a).
afterLeft (b, a) -> afterLeft (b.left, a).
afterLeft (a, b) -> not afterLeft (b, a).
afterLeft (a, b) -> afterLeft (a.right, b).

not beforeRight (a, a).
not beforeRight (a, a.left).
not beforeRight (a, b) -> not beforeRight (a, b.left).
not beforeRight (a, b.left) -> not beforeRight (a, b).

not afterRight (a, a).
not afterRight (a, a.left).
not afterRight (a, b) -> not afterRight (a, b.left).
not afterRight (a, b.left) -> not afterRight (a, b).

beforeRight (a, a.right).
beforeRight (a, b) -> beforeRIght(a, b.right).
beforeRight (a, b) -> not beforeRight (b, a).
beforeRight (a, b) -> beforeRight (a, b.left).

afterRight (a.right, a).
afterRight (a, b) -> afterRight (a.right, b).
afterRight (a, b) -> not afterRight (b, a).
afterRight (a, b) -> afterRight (a.left, b).

not before (a, a).
before (a, a.left).
before (a, a.right).
before (a, b) -> before (a, b.left).
before (a, b) -> before (a, b.right).
before (a, b), a != b -> not before (b, a).
not before (a, b), a != b -> before (b, a).

left (a, b), not beforeLeft (a, b) -> False.
right (a, b), afterLeft (a, b) -> False.
right (a, b), beforeLeft (a, b) -> False.
right (a, b), not beforeRight (a, b) -> False.
left (a, b), beforeRight (a, b) -> False.
left (a, b), afterRight (a, b) -> False.

right (a, b), not before (a, b) -> False.
carryLeft (a, b), not before (a, b) -> False.
carryRight (a, b), not before (a, b) -> False.
