from collections import defaultdict

inventory = lambda : defaultdict(lambda : set())

PUNCTUATION = set("; -> != = ( ) , <".split())
IDENTITY = lambda x: x
TOKEN = 'token label'
MUTE = 'mute'
START = 'START'

# TODO: to ensure parses terminate, we can
# keep track of which rules have been applied to each span
# so that, if you have A -> B (r1) and B -> A (r2), and span [i, j] is
# A, it will become B 'just once', with rule r2.
# But that's not sound.
# Because then it should become A again with rule r1.

# In terms of syntax that does not matter (that just means the two
# preterminals are interchangeable - that are As are also Bs, and viceversa)
# but when adding semantics, endless applications of f(g(f(g(...)))) have
# no reason to converge to anything.

def parsableGrammar(grammarText, actionsMap):
    rules = textToRules(grammarText)
    grammar = grammarFromRules(rules)
    actions = semantics(rules, actionsMap)
    return grammar, actions

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
    lines = [l for l in lines if l]
    for line in lines:
        newRules = lineToRules(line)
        rules += newRules
    return rules

def lineToRules(line):
    tokens, name = lineToTokens(line)
    return tokensToRules(tokens, name)

def lineToTokens(line):

    assert "->" in line and ')' in line and '(' in line # to be sure
    
    rparenIndex = -1 # Index of the last )
    lparenIndex = line.rfind("(")
    line = line[:rparenIndex] # String up to the last (
    
    tokens = [t.strip() for t in line[:lparenIndex].split()]
    tokens = tokens[0:1] + tokens[2:] # Ignore '->'

    name = line[lparenIndex+1:]
    # Handle punctuation here

    return tokens, name

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
    size = len(tokens) + 1

    head = tokens.pop(0)
    left = tokens.pop(0)
    
    while tokens:

        auxiliaryRight = f"{name}[{size - len(tokens)}]"
        
        if len(tokens) == 1:
            right = tokens.pop(0)
            newRules = binary(head, left, right, auxiliaryRight)
            rules += newRules
        
        else:
            newRules = binary(head, left, auxiliaryRight, auxiliaryRight)
            rules += newRules
            head = auxiliaryRight
            left = tokens.pop(0)
        
    return rules

def spansToNode(spansMap):
    pass
    
def grammarFromRules(rules):
    grammar = defaultdict(lambda: [])
    for rule in rules:
        rhs, lhs = rule
        if isUnary(rhs):
            rhs, _ = checkSilent(rhs)
            grammar[rhs].append(lhs)
        if isBinary(rhs):
            left, right = rhs
            left, _ = checkSilent(left)
            right, _ = checkSilent(right)
            rhs = left, right
            grammar[rhs].append(lhs)
    return grammar 

# spanRules[i, j] = {r1, r2, ..., rn}
# if rule in spanRules[i, j]:
#     pass

# TODO: refactor this module, so it's less redundant and coupled
# and makes more sense.

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

    readableSpans = set()
    spans = inventory()

    tokens = [tokenizer(elem) for elem in sequence]

    # Handle leaves

    for index, token in enumerate(tokens):
        tokenSpan = (index, index, token, TOKEN)
        endsAt[index].add(tokenSpan)
        beginsAt[index].add(tokenSpan)
        notVisited.add(tokenSpan)
        readableSpans.add((token, index, index, token))
        leafSpan = (token, TOKEN, index)
        spans[index, index].add(leafSpan)

    # Parse token sequence

    while notVisited:

        currentSpan = notVisited.pop()

        branchBegin, branchEnd, branchLabel, branchRule = currentSpan

        # Handle unary rules

        if branchLabel in ruleTriggers.keys():
            for pair in ruleTriggers[branchLabel]:
                newLabel, newRule = pair
                newSpan = (branchBegin, branchEnd, newLabel, newRule)
                endsAt[branchEnd].add(newSpan)
                beginsAt[branchBegin].add(newSpan)
                notVisited.add(newSpan)
                spanSequence = tuple(sequence[branchBegin:branchEnd+1])
                readableSpans.add((newLabel, branchEnd, branchBegin, " ".join(spanSequence)))
                unarySpan = (newLabel, branchLabel, newRule, branchBegin, branchEnd) # C2 add branch label data to span
                spans[branchBegin, branchEnd].add(unarySpan)

        # Handle binary rules (left case)
        
        leftBegin, leftEnd, leftLabel, leftRule = currentSpan

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
                    
                    spanSequence = tuple(sequence[leftBegin:rightEnd+1])
                    leftSequence = tuple(sequence[leftBegin:leftEnd+1])
                    rightSequence = tuple(sequence[rightBegin:rightEnd+1])

                    readableSpans.add((newLabel, leftBegin, rightEnd, " ".join(spanSequence)))

                    binarySpan = binarySpan = (newLabel, leftLabel, rightLabel, newRule, leftBegin, leftEnd, rightBegin, rightEnd)
                    spans[leftBegin, rightEnd].add(binarySpan)

        # Handle binary rules (right case)

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

                    leftSequence = tuple(sequence[leftBegin:leftEnd+1])
                    rightSequence = tuple(sequence[rightBegin:rightEnd+1])
                    spanSequence = tuple(sequence[leftBegin:rightEnd+1])

                    readableSpans.add((newLabel, leftBegin, rightEnd, " ".join(spanSequence)))
                    binarySpan = (newLabel, leftLabel, rightLabel, newRule, leftBegin, leftEnd, rightBegin, rightEnd)
                    spans[leftBegin, rightEnd].add(binarySpan)

    return spans, readableSpans

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

    spans, readable = cyk(tokens, grammar)

    for span in readable:
        spanLabel, l, r, spanText = span
        print(spanLabel, l, r, spanText)

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
        # You should use the name of the rule, not the label of the head
        head, actionName = lhs

        if isBinary(rhs):

            left, right = rhs
            left, leftIsMute = checkSilent(left)
            right, rightIsMute = checkSilent(right)
            
            if actionName in triggers.keys():
                semanticAction = triggers[actionName]
            else:
                semanticAction = lambda x: x

            if leftIsMute and rightIsMute:
                argumentAction = ignoreBoth
            if leftIsMute and not rightIsMute:
                argumentAction = ignoreLeft
            if not leftIsMute and rightIsMute:
                argumentAction = ignoreRight
            if not leftIsMute and not rightIsMute:
                argumentAction = includeBoth
            
            actions[actionName] = (head, semanticAction, argumentAction)

        if isUnary(rhs):

            production, mute = checkSilent(rhs)
            semanticAction = triggers[actionName]

            if mute:
                argumentAction = lambda x: []
            else:
                argumentAction = lambda x: [x]

            actions[actionName] = (head, semanticAction, argumentAction)

    return actions
                
identity = lambda x: x

testTriggers = {
        'n-ary number' : lambda x: int(x),
        'Parenthesis' : identity,
        'Addition' : lambda x, y: x + y,
        'Substraction' : lambda x, y: x - y,
        'Additive inverse' : lambda x: -x,
        'Multiplication' : lambda x, y: x * y,
        'Decimal digit' : identity,
        'Single digit' : identity,
        'Several digits' : lambda x, y: x + y,
        'Plus symbol' : identity,
        'Minus symbol' : identity,
        'Times symbol' : identity,
        'Left parenthesis' : identity,
        'Right parenthesis' : identity,
        TOKEN : identity
        }

                
testGrammar = '''
    NUMBER -> DIGITS                     (n-ary number)
    NUMBER -> [LPAREN] NUMBER [RPAREN]   (Parenthesis)
    NUMBER -> NUMBER [PLUS] NUMBER       (Addition)
    NUMBER -> NUMBER [MINUS] NUMBER      (Substraction)
    NUMBER -> [MINUS] NUMBER             (Additive inverse)
    NUMBER -> NUMBER [TIMES] NUMBER      (Multiplication)
    LPAREN -> (                          (Left parenthesis)
    RPAREN -> )                          (Right parenthesis)
    DIGIT -> 0                           (Decimal digit)
    DIGIT -> 1                           (Decimal digit)
    DIGIT -> 2                           (Decimal digit)
    DIGIT -> 3                           (Decimal digit)
    DIGIT -> 4                           (Decimal digit)
    DIGIT -> 5                           (Decimal digit)
    DIGITS -> DIGIT                      (Single digit)
    DIGITS -> DIGIT DIGITS               (Several digits)
    PLUS -> +                            (Plus symbol)
    MINUS -> -                           (Minus symbol)
    TIMES -> *                           (Times symbol)
'''

def testGrammarToRules():
    print('\nRules:\n')
    rules = textToRules(testGrammar)
    for rule in rules:
        print(rule)
    print("")
        
def testSemantics():

    grammar, actions = parsableGrammar(testGrammar, testTriggers)
    
    for r in grammar:
        print("Rule:", r, ":", grammar[r])
        
    print("")
        
    for a in actions:
        print("Action:", a, ":", actions[a])
        
    print("")
    
    tokens = "- ( 5 + 4 ) + 1".split()
    spans, _ = cyk(tokens, grammar)
    # result = evaluate(spans, actions, label="NUMBER")

    for r in zip([0],result):
        print("Result: ", r)
        
    print("")
        
def evaluate(i, j, targetLabel, spans, actions):
    
    # values[span][label] = [list of values with label l at span i j]
    # requirements[span] = [pairs of span, label dependencies]

    # pending = [a stack of spans for which you do not yet have a value]
    
    # binarySpan = binarySpan = (newLabel, leftLabel, rightLabel, newRule, leftBegin, leftEnd, rightBegin, rightEnd)

    currentSpan = (i, j, targetLabel)
    
    values = defaultdict(lambda: defaultdict(lambda : []))
    dependencies = defaultdict(lambda: defaultdict(lambda : []))
    dependees = defaultdict(lambda: defaultdict(lambda : []))

    # Set up requirements map
    
    for span in spans:

        # track dependencies
        
        leaf = len(span) == 3
        unary = len(span) = 5
        binary = len(span) == 8
    
        if leaf:
            # Leaves have no dependencies, and are always ready
            # So we compute their value right away
            value[span] = ?( spans [span])
            
        if unary:
            # The head span depends on the branch span
            # The branch span tracks this head span depends on it
            headLabel, branchLabel, rule, i, j = spans[span]
            dependencies[i, j][branchLabel].append((i, j))
            dependees[i, j][headLabel].append((i, j))
        
        if binary:
            # Binary nodes depend on their left and right branches

            headLabel, leftLabel, rightLabel, rule, ll, lr, rl, rr = span
            
            # Track dependency / dependee relations between
            # the head span and its two branches
            dependencies[ll, rr][leftLabel].append((ll, lr))
            dependencies[ll, rr][rightLabel].append((rl, rr))
            dependees[ll, lr][headLabel].append(ll, rr)
            dependees[rl, rr][headLabel].append(ll, rr)

            # Should dependencies be indexed by label
            # or by action name?
    
    targetSpanCoordinates = ?(targetSpan)
    pending.append(targetSpanCoordinates) # (i, j) or (i, j, label) or (i, j, action)

    while targetSpan not in values:

        while pending:

            requirements = [span for span in dependencies[currentSpan] if span not in values]

            pending += requirments

            currentSpan = pending[-1]
            i, j, headLabel = ?(currentSpan)

            if dependenciesMet:

                # Collect branch values
                
                if leaf:
                    argumentValues = ?(currentSpan)

                if unary:
                    argumentValues = ?(currentSpan)
                
                if binary:
                    leftBranch = ?(currentSpan)
                    rightBranch = ?(currentSpan)
                    leftValue = values[leftCoordinates][leftLabel]
                    rightValue = values[rightCoordinates][rightLabel]
                    
                    argumentValues = (leftValue, rightValue)

                # Compute head value
                value = ?(argumentValues)
                values[span] = value # You need to know which action to call, so action name data is needed
                # spans[i, j] contains all the required data, so in any case that can be recovered

                # Update requirement queues and maps

                # Remember to use span coordinates, and
                # not the whole span
                for dependee in dependees[currentSpan]:
                    requirements[dependee].remove((i, j))

                # Pop fulfilled dependency

                pending.remove((i, j, headLabel))

            if not dependenciesMet:

                # Add dependencies to pending

                # update dependencies

                # next iteration

    value = values[fullSpan]

    return value, values

testCYK()
testGrammarToRules()
testSemantics()