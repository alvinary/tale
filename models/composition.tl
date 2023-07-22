order n 50 : node.
order l 100 : leaf.
order v 50 : vertex.
order l 100 : vertex.
order tn 30 : typenode.
order tl 60 : typeleaf.
order tn 30 : type.
order tl 60 : type.
order c 6 : category.
  
-- since types are shared by several
-- nodes, they need not be in a
-- one-to-one correspondence with
-- some f(|vertex|)

let node.type : dummytype.
let node.left : dummyvertex.
let node.right : dummyvertex.
  
let typenode.from : dummytype.
let typenode.to : dummytype.

let assign : dummyvertex -> vertex.
let assign : dummytype -> type.

var t, s : type.
var a, b : vertex.
  
var n, m : node.
var l, f : leaf.
var tn, tm : typenode.
var tl, tf : typeleaf.

var dn, dm : dummyvertex.
var dt, ds : dummytype.

var A, B : category.

-- Composition and type checking
  
match (n.left.type.from, n.right.type) -> matchArgument (n).
match (n.left.right.to, n.type) -> matchReturn (n).

-- matchreturn and not cond -> False.

not matchReturn (n) -> False.
not matchArgument (n) -> False.

cat (tl, A), cat (tf, A) -> match (tl, tf).
cat (tl, A), cat (tf  B), A != B, match (tl  tf) -> False.

match (tn.from, tm.from), match (tn.to, tm.to) -> match (tn, tm).
not match (tn.from, tm.from), match (tn, tm) -> False.
not match (tn.to, tm.to), match (tn, tm) -> False.

-- tree behavior
