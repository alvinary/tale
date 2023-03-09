from collections import defaultdict

PUNCTUATION = set("; -> != = ( ) , <".split())
TOKEN = 'token label'
MUTE = 'mute'
LBRACE = '{'
RBRACE = '}'
NEWLINE = '\n'
COMMENT = '--'
UNORDERED = 10.0

inventory = lambda : defaultdict(lambda : set())

def getLines(text):
    # The first line should be '<separator> <precedence>'
    # This simply takes the first line, splits it at whitespace,
    # and returns whatever it finds after the first token
    firstLine = [l for l in text.split('\n') if l][0]
    lines = text.split('\n')
    lines = [line for line in lines if line and notComment(line)]
    lines = lines[1:]
    
    evaluate = firstLine.split()[0].strip()
    precedence = firstLine.split()[1].strip()
    
    return evaluate, precedence, lines
    
def linesToPrecedence(lines, separator, precedence):
    order = defaultdict(lambda: UNORDERED)
    for index, line in enumerate(lines):
        if precedence in line:
            orderValues = [t for t in line.split() if t.startswith(precedence)]
            orderValue = float(orderValues[0].replace(precedence, ""))
            order[str(index)] = orderValue
            order[str(index) + '[1]'] = orderValue
    return order

def linesToActions(lines, separator, precedence):
    actions = {}
    lines = [l.split(separator)[1].strip() for l in lines]
    for index, line in enumerate(lines):
        actions[str(index)] = (lambda : eval('lambda ' + line)) ()
    return actions

def notComment(line):
    return COMMENT != line[:len(COMMENT)]
    
def removePrecedence(line, precedence):
    if precedence not in line:
        return line
    return " ".join([t for t in line.split() if not t.startswith(precedence)])
    
def linesToRules(lines, separator, precedence):
    # The first line should be separator <separator>
    rules = []
    lines = [removePrecedence(l, precedence).split(separator)[0].strip() for l in lines]
    lines = [l + f' ({i})' for i, l in enumerate(lines)]
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

    head = tokens.pop(0)
    left = tokens.pop(0)
    
    while tokens:

        auxiliaryRight = f"{name}[{len(tokens) - 1}]"
        
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
    
def overlap(i, j, k, l):
    end = max(j, l)
    if end == j:
        return i <= l
    if end == l:
        return k <= j
    
class Parser:
    def __init__(self, grammar):    
        separator, precedence, lines = getLines(grammar)
    
        order = linesToPrecedence(lines, separator, precedence)
        rules = linesToRules(lines, separator, precedence)
        actions = linesToActions(lines, separator, precedence)
        
        
        actions[TOKEN] = lambda x : [x]
        
        self.precedence = order
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
            check = True # Because leaves already have a value

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
            _, action, arg = self.actions[head[3]] # Magic number 3
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

def pairs(sequence):
    for i in range(len(sequence)):
        for j in range(i):
            yield (sequence[i], sequence[j])

def getHead(span):
    return span[0]
        
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

        self.prune()
                 
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

    def compare(self, left, right):
        leftLabel, i, j, leftName = left
        rightLabel, k, l, rightName  = right
        leftPrecedence = self.parser.precedence[leftName]
        rightPrecedence = self.parser.precedence[rightName]
        if leftLabel == rightLabel and i == k and j == l and leftPrecedence != rightPrecedence:
            if leftPrecedence < rightPrecedence:
                return left
            if rightPrecedence < leftPrecedence:
                return right
        else:
            return False
        
    def prune(self):
    
        remove = set()
        nodes = set()

        for indices in self.spans:
            for span in self.spans[indices]:
                nodes |= set(span)

        nodes = list(nodes)
        
        for n, m in pairs(nodes):
            comparison = self.compare(n, m)
            if comparison:
                remove.add(comparison)

        for indices in self.spans:
            spanItems = self.spans[indices]
            self.spans[indices] = [i for i in spanItems if i not in remove]
            


