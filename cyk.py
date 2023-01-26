from collections import defaultdict

inventory = lambda : defaultdict(lambda : set())

PUNCTUATION = set("; -> != = ( ) , <".split())
IDENTITY = lambda x: x
TOKEN = 'token label'
MUTE = 'mute'

# Ignored arguments now have []. How do we handle that?
# While creating auxiliary rules, one can create auxiliary
# semantic actions. So one should return those.

# Since the set of auxiliary and real rules are disjoint,
# it's not necessary to pass the whole map of semantic actions:
# Auxiliary rules either ignore or append, which means you don't
# need any information about the implementation of the functions
# used by 'real' nodes.

def parsableGrammar(grammarText, actionsMap):
    rules = textToRules(grammarText)
    grammar = grammarFromRules(rules)
    actions = semantics(rules, actionsMap)
    return grammar, actions

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

def textToRules(text):
    
    '''

    map rule names to functions

    lambda x: f(x)
    lambda x, y : f (x, y)

    vs

    f(*args)

    Auxiliary nodes only ignore or append arguments.
    'Real' nodes call their apply method on the list
    of arguments assembled bottom-up.

    '''

    rules = []
    lines = [l.strip() for l in text.split("\n")]
    for line in lines:
        if line:
            rules += lineToRules(line)
    return rules

def lineToRules(line):
    tokens, name = lineToTokens(line)
    return tokensToRules(tokens, name)

def lineToTokens(line):

    assert "->" in line and ')' in line and '(' in line # to be sure
    
    line = line[:-1] # Remove ')'
    tokens, name = tuple(line.split("("))

    # Handle punctuation here

    tokens = [p.strip() for p in tokens.split()]
    head = tokens[0:1]
    tokens = tokens[2:] # Ignore '->'
    return head + tokens, name

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
    return [((left, right), (head, name))]

def unary(head, branch, name):
    return [(branch, (head, name))]

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
    
def grammarFromRules(rules):
    grammar = {}
    for rule in rules:
        rhs, lhs = rule
        if isUnary(rhs):
            rhs, _ = checkSilent(rhs)
            grammar[rhs] = lhs
        if isBinary(rhs):
            left, right = rhs
            left, _ = checkSilent(left)
            right, _ = checkSilent(right)
            rhs = left, right
            grammar[rhs] = lhs
    return grammar 

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

def testGrammarToRules():
    grammar = '''
    NUMBER -> DIGITS                     (n-ary number)
    NUMBER -> [LPAREN] NUMBER [RPAREN]   (Parenthesis)
    NUMBER -> NUMBER PLUS NUMBER         (Addition)
    NUMBER -> NUMBER MINUS NUMBER        (Substraction)
    NUMBER -> MINUS NUMBER               (Additive inverse)
    NUMBER -> NUMBER TIMES NUMBER        (Multiplication)
    DIGIT -> 0                           (Binary digit)
    DIGIT -> 1                           (Binary digit)
    DIGITS -> DIGIT                      (Single digit)
    DIGITS -> DIGIT DIGITS               (Several digits)
    PLUS -> +                            (Plus symbol)
    MINUS -> -                           (Minus symbol)
    TIMES -> *                           (Times symbol)
    '''

    print('\nRules:\n')
    for rule in textToRules(grammar):
        print(rule)

def checkSilent(token):
    if token[0] == "[" and token[-1] == "]":
        return token[1:-1], True
    else:
        return token, False
        
def isUnary(rhs):
    return not isinstance(rhs, tuple)

def isBinary(rhs):
    return isinstance(rhs, tuple) and len(rhs) == 2

def semantics(grammar, triggers):

    encapsulate = lambda x : [x]
    ignoreLeft = lambda x, y : y
    ignoreRight = lambda x, y : x
    ignoreBoth = lambda x, y : []
    includeBoth = lambda x, y : x + y

    actions = {}

    for rule in grammar:
        
        rhs, lhs = rule
        head, actionName = rhs

        if isBinary(rhs):

            left, right = rhs
            left, leftIsMute = checkSilent(left)
            right, rightIsMute = checkSilent(right)
            semanticAction = triggers[actionName]

            if leftIsMute and rightIsMute:
                argumentAction = ignoreBoth
            if leftIsMute and not rightIsMute:
                argumentAction = ignoreLeft
            if not leftIsMute and rightIsMute:
                argumentAction = ignoreRight
            if not leftIsMute and not rightIsMute:
                argumentAction = includeBoth
            
            actions[left, right] = (head, semanticAction, argumentAction)

        if isUnary(rhs):

            production, mute = checkSilent(rhs)
            semanticAction = triggers[actionName]

            if mute:
                argumentAction = lambda x: []
            else:
                argumentAction = lambda x: [x]

            actions[production] = (head, semanticAction, argumentAction)

    return actions
    
def label(span):
    return span[0]

def evaluate(spans, semantics, l=START, i=0, j=0):
    '''
    semantics[ruleName] = lambda x, y : f (x, y)

    spans[i, j] = [(label, rule, apply, leftLabel, rightLabel, i, k, j)]
                + [(label, rule, apply, branchLabel, i, j)]
    '''

    # if i and j are not specified...

    minIndex = min([leftIndex(span) for _, span in spans])
    maxIndex = max([rightIndex(span) for _, span in spans])

    fullSpan = minIndex, maxIndex

    feasibleSpans = [span for span in spans[i, j] if label(span) == targetLabel]

    for span in feasibleSpans:

        # unary = ?(span)
        # binary = ?(span)
        # leaf = ?(span)

        if leaf:
            # apply, token = ?(span)
            yield apply(token)

        if unary:
            feasible = evaluate(spans, semantics, l=branchLabel, i=i, j=j)
            for branch in feasible:
                # apply = ?(span)
                yield apply(branch)

        if binary:
            # k, leftLabel, rightLabel = ?(span)
            leftSpans =  evaluate(spans, semantics, l=leftLabel, i=i, j=k)
            rightSpans = evaluate(spans, semantics, l=rightLabel, i=k, j=j)
            for left, right in product(leftSpans, rightSpans):
                # apply = ?(span)
                yield apply(left, right)


testCYK()
testGrammarToRules()
testSemantics()
testEvaluation()
