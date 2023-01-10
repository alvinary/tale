from collections import defaultdict

inventory = lambda : defaultdict(lambda : set())

PUNCTUATION = set(";->!=(),<")
IDENTITY = lambda x: x
TOKEN = 'token label'

def ignore(*args):
    return []

class ParseTree():
    def __init__(self):
        pass

class BinaryNode(ParseTree):
    def __init__(self, left, right, apply):
        self.left = left
        self.right = right
        self.apply = apply

    def evaluate(self):
        arguments = self.left.evaluate() + self.right.evaluate()
        return self.apply(*arguments)

class UnaryNode(ParseTree):
    def __init__(self, branch, apply):
        self.branch = branch
        self.apply = apply

    def evaluate(self):
        return self.apply(self.branch.evaluate())

class Leaf(ParseTree):
    def __init__(self, data, apply):
        self.data = data
        self.apply = apply

    def evaluate(self):
        return self.apply(self.data)

def isPunctuation(character):
    return character in PUNCTUATION

def curryRule(left, right, name):
    auxiliaryRules = []
    # A -> B C D  (name)
    # A -> B A[name 1]
    # A[name 1] -> C D
    #
    # 1 -> 2 3 4 5 (name)
    # 1 -> 2 1[name, 1]
    # 1[name, 1] -> 3 1[2]
    # 1[name, 2] -> 4 5

    # apply = [] + []

    return auxiliaryRules

def grammarToRules(text, functionMap):
    '''
    map rule names to functions

    lambda x: f(x)
    lambda x, y : f (x, y)

    vs

    f(args)

    dynamic checks?

    '''
    rules = []
    return rules

def lineToRules(line):
    rule(tokens(line))

def lineToTokens(line):
    split
    ignore
    return

def tokensToRules(tokens, name):
    if len(tokens) == 3:
        head, left, right = tuple(tokens)
        return binary(head, left, right, name)
    if len(tokens) == 2:
        head, branch = tuple(tokens)
        return unary(head, branch, name)
    if len(tokens) > 3:
        return nary(tokens, name)

def binary(head, left, right, name):
    return ((left, right), (head, name))

def unary(head, branch, name):
    return (branch, (head, name))

def nary(tokens, name):

    rules = []
    count = 0

    head = tokens.pop(0)
    left = tokens.pop(0)
    
    while tokens:
        count += 1
        auxiliaryRight = f"{name}[{count}]"
        if len(tokens) == 1:
            right = tokens.pop(0)
            rule = binary(head, left, right, auxiliaryRight)
            rules.append(rule)
        else:
            rule = binary(head, left, auxiliaryRight, auxiliaryRight)
            rules.append(rule)
            head = auxiliaryRight
            left = tokens.pop(0)
        
    return rules

def spansToNode(spansMap):
    pass

# Write a function that turns grammars with rules
# whose right hand side has more than two preterminals
# (currying rules with more than two productions) into
# grammars with unary and binary rules, since it's 
# horrible to write grammars with only binary rules

def cyk(sequence, ruleTriggers, tokenizer=IDENTITY):

    # RuleTriggers should be a map from (label str, label str) to
    # (label str, rule str) and (label str) to (label str, rule str),
    # so that if the following rules are in the grammar,

    # NUMBER -> NUMBER NEGNUMBER  (substraction)
    # NUMBER -> NUMBER PLUSNUMBER (addition)
    # NEGNUMBER -> MINUS NUMBER   (minus n)
    # PLUSNUMBER -> PLUS NUMBER   (plus n)
    # NUMBER -> NEGNUMBER         (additive inverse)
    # NUMBER -> DIGITS            (literal)
    # DIGITS -> DIGIT DIGITS      (several digits)
    # DIGITS -> DIGIT             (single digit)
    # PLUS -> +                   (plus symbol)
    # MINUS -> -                  (minus symbol)
    # DIGIT -> 0 | 1 | 2 | 3 | 4
    #        | 5 | 6 | 7 | 8 | 9  (decimal digits)

    # then ruleTriggers is

    # (NUMBER, NEGNUMBER)  -> (NUMBER, substraction)
    # (NUMBER, PLUSNUMBER) -> (NUMBER, addition)
    # (MINUS, NUMBER)      -> (NEGNUMBER, minus n)
    #         ...          ->         ...
    # +                    -> (PLUS, plus symbol)
    # -                    -> (MINUS, minus symbol)
    # 0                    -> (DIGIT, decimal digits)
    # 1                    -> (DIGIT, decimal digits)
    #         ...          ->         ...

    notVisited = set()
    endsAt = inventory()
    beginsAt = inventory()

    spans = set()

    tokens = [tokenizer(elem) for elem in sequence]
    # This might require a function argument to be more general

    for index, token in enumerate(tokens):
        tokenSpan = (index, index, token, TOKEN)
        endsAt[index].add(tokenSpan)
        beginsAt[index].add(tokenSpan)
        notVisited.add(tokenSpan)
        spans.add((token, " ".join(sequence[index:index+1])))

    while notVisited:

        currentSpan = notVisited.pop()

        leftBegin, leftEnd, leftLabel, leftRule = currentSpan
        
        if leftLabel in ruleTriggers.keys():
            for pair in ruleTriggers[leftLabel]:
                newLabel, newRule = pair
                newSpan = (leftBegin, leftEnd, newLabel, newRule)
                endsAt[leftEnd].add(newSpan)
                beginsAt[leftBegin].add(newSpan)
                notVisited.add(newSpan)
                spans.add((newLabel, " ".join(sequence[leftBegin:leftEnd+1])))

        candidates = set(beginsAt[leftEnd + 1])

        for candidate in candidates:
            rightBegin, rightEnd, rightLabel, rightRule = candidate
            production = (leftLabel, rightLabel)
            if production in ruleTriggers.keys():
                for newLabel, newRule in ruleTriggers[production]:
                    newSpan = (leftBegin, rightEnd, newLabel, newRule)
                    beginsAt[leftBegin].add(newSpan)
                    endsAt[rightEnd].add(newSpan)
                    notVisited.add(newSpan)
                    spans.add((newLabel, " ".join(sequence[leftBegin:rightEnd+1])))

        rightBegin, rightEnd, rightLabel, rightRule = currentSpan
        candidates = set(endsAt[rightBegin - 1])

        for candidate in candidates:
            leftBegin, leftEnd, leftLabel, leftRule = candidate
            production = (leftLabel, rightLabel)
            if production in ruleTriggers.keys():
                for newLabel, newRule in ruleTriggers[production]:
                    newSpan = (leftBegin, rightEnd, newLabel, newRule)
                    beginsAt[leftBegin].add(newSpan)
                    endsAt[rightEnd].add(newSpan)
                    notVisited.add(newSpan)
                    spans.add((newLabel, " ".join(sequence[leftBegin:rightEnd+1])))

    return spans

def testCYK():

    tokens = "- ( 5 + 4 ) + 1".split()

    grammar = {
               '5' : [("NUMBER", "Single digit")],
               '4' : [("NUMBER", "Single digit")],
               '1' : [("NUMBER", "Single digit")],
               '(' : [("LPAREN", "( symbol")],
               ')' : [("RPAREN", ") symbol")],
               '+' : [("PLUS", "+ symbol")],
               '-' : [("MINUS", "- symbol")],
               ('PLUS', 'NUMBER') : [("PLUSNUMBER", "Addition")], 
               ('MINUS', 'NUMBER') : [("NUMBER", "Additive inverse")],
               ('NUMBER', 'PLUSNUMBER') : [("NUMBER", "Sum")],
               ('LPAREN', 'PARENNUMBER') : [("NUMBER", "Closing parentheses")],
               ('NUMBER', 'RPAREN') : [("PARENNUMBER", "Opening parentheses")]
            }

    for span in cyk(tokens, grammar):
        spanLabel, spanText = span
        print(spanLabel, spanText)

testCYK()
