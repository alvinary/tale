from collections import defaultdict

PUNCTUATION = set("; -> != = ( ) , <".split())
TOKEN = 'token label'
MUTE = 'mute'

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
    
class Parser:
    def __init__(self, grammar, actions):
        rules = textToRules(grammar)
        self.grammar = grammarFromRules(rules)
        self.actions = semantics(rules, actions)
        
    def parse(self, tokens):
        return Parse(tokens, self).execute()
         
    def value(self, tokens):
        parse = Parser(tokens, self).execute()
        result = None
        return result
        
class Parse:
    def __init__(self, tokens, parser):
        self.parser = parser
        self.tokens = tokens
        self.unvisited = set()
        self.added = set()
        self.endAt = inventory()
        self.beginAt = inventory()
        self.spans = inventory()
        
        self.readable = set()
        
    def execute(self):
    
        for index, token in enumerate(self.tokens):
            self.addToken(index, token)
            self.spans[index, index].add((token, index, index, TOKEN))
             
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
                self.addSpan(label, begin, end, action)
                self.spans[begin, end].add((label, begin, end, action))
        else:
            pass
                 
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
        else:
            pass
     
    def addSpan(self, label, begin, end, action):
        spanData = (label, begin, end, action)
        self.endAt[end].add(spanData)
        self.beginAt[begin].add(spanData)
        if spanData not in self.added:
            self.unvisited.add(spanData)
            self.added.add(spanData)
        spanContent = tuple(self.tokens[begin:end+1])
        self.readable.add((label, spanContent))
        
    def addToken(self, index, token):
        self.addSpan(token, index, index, TOKEN)

