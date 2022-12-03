order lv 10 : level.
order c 8 : constant.

var a, b : constant.
var l, v : level.

let level : constant -> level.

level (c0, lv0).
after (a, a) -> False.
after (a, b) -> after (a, b.next).
after (a, b), after (b, a) -> False.
level (a, l), level (a.next, v), v != l.next -> False.

level (a, l), level (a, v), v != l -> False.
level (a, l), level (b, l), a != b -> False.
