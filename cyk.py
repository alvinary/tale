from collections import defaultdict

PUNCTUATION = set("; -> != = ( ) , <".split())
TOKEN = 'token label'
MUTE = 'mute'
LBRACE = '{'
RBRACE = '}'

inventory = lambda : defaultdict(lambda : set())
    
def textToRules(grammarText):
    rules = []
    lines = [l.strip() for l in grammarText.split("\n")]
    lines = [l for l in lines if l]
    for line in lines:
        newRules = lineToRules(line)
        rules += newRules
    return rules
    
def lineToRules(line):
    tokens, name = lineToParts(line)
    return tokensToRules(tokens, name)

def lineToParts(line):
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

    '''
       Input a sequence of tokens and a rule
       name and return the corresponding rule.
    '''
    
    if tokens[1] == LBRACE and tokens[-1] == RBRACE:
        rules = []
        head = tokens[0]
        members = tokens[2:-1] # ignore '{' and '}'
        members = [s.strip() for s in ''.join(members).split(',')] # Remove commas
        for leaf in members[1:]:
            rules += unaryRule(head, leaf, name)
        return rules

    if len(tokens) == 2:
        head, branch = tuple(tokens)
        return unaryRule(head, branch, name)

    if len(tokens) == 3:
        head, left, right = tuple(tokens)
        return binaryRule(head, left, right, name)
    
    if len(tokens) > 3:
        return naryRule(tokens, name)
        
def binaryRule(head, left, right, name):
    return [((left, right), (head, name))]

def unaryRule(head, branch, name):
    return [(branch, (head, name))]

def naryRule(tokens, name):

    rules = []
    size = len(tokens) + 1

    head = tokens.pop(0)
    left = tokens.pop(0)
    
    while tokens:

        auxiliaryRight = f"{name}[{size - len(tokens)}]"
        
        if len(tokens) == 1:
            right = tokens.pop(0)
            newRules = binaryRule(head, left, right, auxiliaryRight)
            rules += newRules
        
        else:
            newRules = binaryRule(head, left, auxiliaryRight, auxiliaryRight)
            rules += newRules
            head = auxiliaryRight
            left = tokens.pop(0)
        
    return rules
    
    
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

    encapsulate = lambda x : x
    ignoreLeft = lambda x, y : y
    ignoreRight = lambda x, y : x
    ignoreBoth = lambda x, y : []
    includeBoth = lambda x, y : x + y

    actions = {}

    for rule in grammar:
        
        rhs, lhs = rule
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
                argumentAction = lambda x: x

            actions[actionName] = (head, semanticAction, argumentAction)

    return actions
    
class Parser:
    def __init__(self, grammar, actions):
        rules = textToRules(grammar)
        self.grammar = grammarFromRules(rules)
        self.actions = semantics(rules, actions)
        self.values = {}
        
    def parse(self, tokens):
        return Parse(tokens, self).execute()
        
    def setValue(self, span):
    
        if span[0] in self.values: # Value is already stored
            return
            
        isLeaf = len(span) == 1
        isUnary = len(span) == 2
        isBinary = len(span) == 3
    
        if isLeaf:
            leaf = span[0]
            check = True # The token

        if isUnary:
            head, branch = span
            check = branch in self.values

        if isBinary:
            head, left, right = span
            check = left in self.values
            check = check and right in self.values
        
        if check and isLeaf:
            self.values[leaf] = leaf[0] # The token
            
        if check and isUnary:
            _, action, arg = self.actions[head[3]]
            argument = self.values[branch]
            self.values[head] = action(arg(argument))
        
        if check and isBinary:
            _, action, args = self.actions[head[3]]
            left = self.values[left]
            right = self.values[right]
            self.values[head] = action(args(left, right))
        
        # TODO: add error messages so this function
        # provides useful information when something
        # goes wrong, instead of failing silently
         
    def value(self, tokens):
        
        parse = self.parse(tokens)
        
        distances = set()

        leaves = defaultdict(lambda: [])
        binary = defaultdict(lambda: [])
        unary = defaultdict(lambda: [])
        
        for span in parse.spans.keys():
            distance = span[1] - span[0]
            data = parse.spans[span]
            for d in data:
                if len(d) == 1:
                    leaves[distance].append(d)
                if len(d) == 2:
                    unary[distance].append(d)
                if len(d) == 3:
                    binary[distance].append(d)    
            distances.add(distance)
            
        for span in leaves[0]:
            self.setValue(span)
        
        for k in sorted(distances):
            for s in binary[k]:
                for t in binary[k]:
                    self.setValue(t)
            
            for s in binary[k]:
                head, _, _ = s
                    
            for s in unary[k]:
                for t in unary[k]:
                    self.setValue(t)
                    
            for s in unary[k]:
                head, _ = s

        begin = 0
        end = max(distances)
        
        fullSpans = [span for span in self.values if span[1] == begin and span[2] == end]
            
        results = [self.values[k] for k in fullSpans]
        
        return results
        
class Parse:
    def __init__(self, tokens, parser):
        self.parser = parser
        self.tokens = tokens
        self.unvisited = set()
        self.endAt = inventory()
        self.beginAt = inventory()
        self.spans = inventory()
        
        self.readable = set()
        
    def execute(self):
    
        for index, token in enumerate(self.tokens):
            self.addToken(index, token)
            self.spans[index, index].add(((token, index, index, TOKEN),))
             
        while self.unvisited:
            current = self.unvisited.pop()
            label, begin, end, action = current 
            self.trigger(current)
            
            left = set(self.endAt[begin-1])
            for other in left:
                self.triggerPair(other, current)
                
            right = set(self.beginAt[end+1])
            for other in right:
                self.triggerPair(current, other)
                 
        return self
        
    def trigger(self, branch):
        branchLabel, begin, end, branchAction = branch
        if (branchLabel) in self.parser.grammar.keys():
            for pair in self.parser.grammar[branchLabel]:
                label, action = pair
                head = (label, begin, end, action)
                self.addSpan(label, begin, end, action)
                self.spans[begin, end].add((head, branch))
                 
    def triggerPair(self, left, right):
        lLabel = left[0]
        rLabel = right[0]
        begin = left[1]
        end = right[2]
        if (lLabel, rLabel) in self.parser.grammar.keys():
            for pair in self.parser.grammar[(lLabel, rLabel)]:
                label, action = pair
                head = label, begin, end, action
                self.addSpan(*head)
                self.spans[begin, end].add((head, left, right))
     
    def addSpan(self, label, begin, end, action):
        spanData = (label, begin, end, action)
        self.endAt[end].add(spanData)
        self.beginAt[begin].add(spanData)
        self.unvisited.add(spanData)
        spanContent = tuple(self.tokens[begin:end+1])
        self.readable.add((label, spanContent))
        
    def addToken(self, index, token):
        self.addSpan(token, index, index, TOKEN)
        
