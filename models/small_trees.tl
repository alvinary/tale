order v 90 : vertex.
let parent : vertex -> vertex.

var a, b : vertex.

before (a, a.next).
before (a, b) -> before (a, b.next).
edge (a, b), before (b, a) -> False.

parent (a, a) -> root (a).
root (a), root (b), a != b -> False.
