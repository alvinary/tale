order lv 10 : level.
order c 8 : constant.

var a, b : constant.
var l : level.

let level : constant -> level.

level (c0, lv0).
after (a, a).
after (a, b) -> after (a, b.next).
after (a, b), after (b, a), a != b -> False.
not after (c0, a) -> False.
level (a, l) -> level (a.next, l.next).
