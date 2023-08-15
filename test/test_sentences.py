from tale.pipeline import *
from tale.objects import *

MODELS = 1

program = '''
order n 5 : node.
order t 6 : leaf.
order n 5 : vertex.
order t 6 : vertex.

num, numop, unum, numb : category.
r1, r2, r3 : rule.
zero, one, two, three, plus, times, minus : terminal.

order i 6 : index.

var A : category.
var a, b : vertex.
var n, m : node.
var t, s : leaf.
var o : terminal.
var i : index.
var r : rule.

let cat : vertex -> category.
let cat : rule -> category.

let rleftCat : rule -> category.
let rrightCat : rule -> category.

let leftCat : node -> category.
let rightCat : node -> category.

let rule : node -> rule.
let terminal : leaf -> terminal.

let left : node -> vertex.
let right : node -> vertex.

let ileft : vertex -> node.
let iright : vertex -> node.

let level : vertex -> index.

-- Constraints on node categories

rule (n, r), cat (r, A) -> cat (n, A).
rule (n, r), cat (r, A), not cat (n, A) -> False.

rule (n, r), rleftCat (r, A) -> leftCat (n, A).
rule (n, r), rrightCat (r, A) -> rightCat (n, A).

rule (n, r), rleftCat (r, A), not leftCat (n, A) -> False.
rule (n, r), rrightCat (r, A), not rightCat (n, A) -> False.

-- Left cat and right cat

left (n, a), cat (a, A) -> leftCat (n, A).
leftCat (n, A), left (n, a), not cat (a, A) -> False.

right (n, a), cat (a, A) -> rightCat (n, A).
rightCat (n, A), right (n, a), not cat (a, A) -> False.

-- Constraints on leaf categories

terminal (t, o), cat (o, A) -> cat (t, A).
terminal (t, o), cat (o, A), not cat (t, A) -> False.

-- Tree behavior

left (a, a) -> False.
right (a, a) -> False.

right (t, a) -> False.
left (t, a) -> False.

left (n, a) -> ileft (a, n).
right (n, a) -> iright (a, n). 

left (a, b), right (a, b) -> False.

right (n, a) -> isRight (a).
left (n, a) -> isLeft (a).

isLeft (a), isRight (a) -> False.

left (a, b), level (a, i) -> level(b, i.next).
right (a, b), level (a, i) -> level(b, i.next).
left (a, b), level (b, i.next) -> level(a, i).
right (a, b), level (b, i.next) -> level(a, i).

level (a, i.next) -> not before (a, i).
not before (a, i.next) -> not before (a, i).
level (a, i) -> before (a, i.next).
before (a, i) -> before (a, i.next).

-- Test rules

-- Labels of terminals

cat (zero, num).
cat (one, num).
cat (two, num).
cat (three, num).
cat (plus, numop).
cat (times, numop).
cat (minus, unum).

-- Rules

cat (r1, num).
rleftCat (r1, num).
rrightCat (r1, numb).

cat (r2, numb).
rleftCat (r2, numop).
rrightCat (r2, num).

cat (r3, num).
rleftCat (r3, unum).
rrightCat (r3, num).

'''


def test_sentences():

    sentences = set()

    for i in range(MODELS):
        models = pipeline(program)
        for i, model in zip(range(1), models):
            sentence = getSentence(model)
            sentences.add(sentence.show().replace("(", "").replace(")", ""))
            
    for s in sentences:
        print(s)

test_sentences()
