from tale.pipeline import *
from tale.objects import *

MODELS = 1

def rules(productions):
    productions = productions.split(".")
    rule_names = list()
    label_names = set()
    terminal_names = set()
    text = ''
    for index, rule in enumerate(productions):
         rule_name = f"r{index}"
         rule = rule.replace("->", "")
         labels = rule.split()
         if len(labels) == 3:
             text += f"cat({rule_name}, {labels[0]}).\nrleftCat({rule_name}, {labels[1]}).\nrrightCat({rule_name}, {labels[2]}).\n"
             label_names |= set(labels)
             rule_names.append(rule_name)
         if len(labels) == 2:
             text += f"cat({labels[1]}, {labels[0]}).\n"
             label_names.add(labels[0])
             terminal_names.add(labels[1])
    return rule_names, list(label_names), list(terminal_names), text

grammar_productions = '''
Num -> zero.
Num -> one.
Num -> two.
Num -> three.
Num -> Num NumBar.
NumBar -> NumOp Num.
NumOp -> times.
NumOp -> plus.
NumOp -> minus.
UNum -> negative.
Num -> UNum Num.
'''

'''
N -> Paulo.
N -> Monsi.
N -> Genaro.
N -> Martina.

V -> hates.
V -> knows.
V -> loves.

S -> NP VP.

VP -> V CP.
VP -> V NP.

NP -> Det NBar.
NP -> Det N.
NP -> Det NBar.
NP -> A N.

NBar -> A N.

CP -> C S.

C -> that.

Det -> certain.

A -> kind.
A -> lovely.
'''

rule_names, label_names, terminal_names, text = rules(grammar_productions)

n = 8

print(rule_names)
print(text)

program = f'''
order n {n} : node.
order t {n+1} : leaf.
order n {n} : vertex.
order t {n+1} : vertex.

{', '.join(label_names)} : category.
{', '.join(rule_names)} : rule.
{', '.join(terminal_names)} : terminal.

order i {n+1} : index.

var AA : category.
var a, b : vertex.
var n, m : node.
var t, s : leaf.
var o : terminal.
var i : index.
var r : rule.

let cat : vertex -> category.
let cat : rule -> category.
let cat : terminal -> category.

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

rule (n, r), cat (r, AA) -> cat (n, AA).
rule (n, r), cat (r, AA), not cat (n, AA) -> False.

rule (n, r), rleftCat (r, AA) -> leftCat (n, AA).
rule (n, r), rrightCat (r, AA) -> rightCat (n, AA).

rule (n, r), rleftCat (r, AA), not leftCat (n, AA) -> False.
rule (n, r), rrightCat (r, AA), not rightCat (n, AA) -> False.

-- Left cat and right cat

left (n, a), cat (a, AA) -> leftCat (n, AA).
leftCat (n, AA), left (n, a), not cat (a, AA) -> False.

right (n, a), cat (a, AA) -> rightCat (n, AA).
rightCat (n, AA), right (n, a), not cat (a, AA) -> False.

-- Constraints on leaf categories

terminal (t, o), cat (o, AA) -> cat (t, AA).
terminal (t, o), cat (o, AA), not cat (t, AA) -> False.

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

-- Root must be a sentence

not cat (n1, Num) -> False.

-- Test rules

{text}

'''

print()
print(program)
print()


def test_sentences():

    sentences = set()

    for i in range(MODELS):
        models = Program(program).models()
        for i, model in zip(range(1), models):
            sentence = getSentence(model)
            sentences.add(sentence.show().replace("(", "").replace(")", ""))
            
    for s in sentences:
        print(s)

test_sentences()
