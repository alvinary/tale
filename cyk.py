from collections import defaultdict

PUNCTUATION = set("; -> != = ( ) , <".split())
TOKEN = 'token label'
MUTE = 'mute'
LBRACE = '{'
RBRACE = '}'
NEWLINE = '\n'
TAB = '\t'
SPACE = ' '
COMMENT = '--'
UNORDERED = 10.0

class ArgumentList:
    def __init__(self, item, ignore=False, next=False):
        self.item = item
        self.nextArgument = next
        self.ignore = ignore
        
    def fromList(arguments):
        # This method assumes 'arguments' is not empty
        argumentList = ArgumentList(arguments.pop(0))
        if arguments:
            argumentList.nextArgument = ArgumentList.fromList(arguments)
        return argumentList
        
    def collect(self):
        if self.ignore and self.nextArgument:
            return self.nextArgument.collect()
        if self.ignore and not self.nextArgument:
            return []
        if not self.ignore and self.nextArgument:
            args = self.nextArgument.collect()
            args.append(self.item)
            return args
        else:
            return [self.item]
        
    def size(self):
        if self.nextArgument:
            return 1 + self.nextArgument.size()
        else:
            return 1
        

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
            order[str(index) + '[0]'] = orderValue # In case a rule is n-ary and the actual rule used during parsing is n[0]
    return order


def linesToActions(lines, separator, precedence):
    actions = {}
    lines = [l.split(separator)[1].strip() for l in lines]
    for index, line in enumerate(lines):
        actions[str(index)] = eval('lambda ' + line)
        
    actions['NEWLINE'] = lambda x : NEWLINE
    actions['SPACE'] = lambda x : SPACE
    actions['TAB'] = lambda x : TAB
        
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
    lines = [
        removePrecedence(l, precedence).split(separator)[0].strip()
        for l in lines
    ]
    lines = [l + f' ({i})' for i, l in enumerate(lines)]
    for line in lines:
        newRules = lineToRules(line)
        rules += newRules
        
    rules += whitespaceRules
    
    return rules


def lineToRules(line):
    tokens, name = lineToParts(line)
    return tokensToRules(tokens, name)


def lineToParts(line):
    assert "->" in line and ')' in line and '(' in line  # to be sure

    rparenIndex = -1  # Index of the last )
    lparenIndex = line.rfind("(")
    line = line[:rparenIndex]  # String up to the last (

    tokens = [t.strip() for t in line[:lparenIndex].split()]
    tokens = tokens[0:1] + tokens[2:]  # Ignore '->'

    name = line[lparenIndex + 1:]
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
        members = tokens[2:-1]  # ignore '{' and '}'
        members = [s.strip()
                   for s in ''.join(members).split(',')]  # Remove commas
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
    size = len(tokens)

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
    
# Argument accumulators

# We pass these instead of Python sequences because
# when working with collections f(*a) could be applied
# to what is intended to be single argument, but happens
# to be a Python sequence
    
def ignoreBoth(x, y):
    if not isinstance(y, ArgumentList):
        y = ArgumentList(y)
    y.ignore = True
    x = ArgumentList(x, ignore=True, next=y)
    return x
    
def ignoreLeft(x, y):
    if not isinstance(y, ArgumentList):
        y = ArgumentList(y)
    x = ArgumentList(x, ignore=True, next=y)
    return x
    
def ignoreRight(x, y):
    if not isinstance(y, ArgumentList):
        y = ArgumentList(y)
    y.ignore = True
    x = ArgumentList(x, ignore=False, next=y)
    return x
    
def includeBoth(x, y):
    if not isinstance(y, ArgumentList):
        y = ArgumentList(y)
    y.ignore = False
    x = ArgumentList(x, ignore=False, next=y)
    return x        
    
def encapsulate(x):
   if not isinstance(x, ArgumentList):
       return ArgumentList(x)
   else:
       return x
   
def emptyArgument(x):
   if not isinstance(x, ArgumentList):
       return ArgumentList(x, ignore=True)
   else:
       x.ignore = True
       return x
       
def variadicIdentity(*x):
    if len(x) > 1:
        return ArgumentList.fromList(list(x))
    else:
        return x[0]

def semantics(grammar, triggers):

    actions = {}
    
    triggers['tab'] = lambda x : x
    triggers['space'] = lambda x : x
    triggers['newline'] = lambda x : x

    for rule in grammar:

        rhs, lhs = rule
        head, actionName = lhs

        if isBinary(rhs):

            left, right = rhs
            left, leftIsMute = checkSilent(left)
            right, rightIsMute = checkSilent(right)

            if actionName in triggers.keys():
                semanticAction = triggers[actionName]

            elif '[0]' in actionName:
                name = actionName.replace('[0]', '')
                semanticAction = triggers[name]

            else:
                semanticAction = variadicIdentity

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
                argumentAction = emptyArgument
            else:
                argumentAction = encapsulate

            actions[actionName] = (head, semanticAction, argumentAction)

    return actions

justToken = lambda x: TOKEN

def parserFromGrammar(grammar, tag=justToken):
    separator, precedence, lines = getLines(grammar)
    order = linesToPrecedence(lines, separator, precedence)
    rules = linesToRules(lines, separator, precedence)
    actions = linesToActions(lines, separator, precedence)
    sem = semantics(rules, actions)
    syn = grammarFromRules(rules)
    return Parser(syn, sem, order, tag=tag)

class Parser:

    def __init__(self, grammar, actions, order, tag=justToken):
        self.precedence = order
        self.grammar = grammar
        self.actions = actions
        self.values = {}
        self.tag = tag

    def parse(self, tokens):
        return Parse(tokens, self).execute()

    def setValue(self, span):

        if span[0] in self.values:  # Value is already stored
            return

        isLeaf = len(span) == 1
        isUnary = len(span) == 2
        isBinary = len(span) == 3

        if isLeaf:
            leaf = span[0]
            check = True  # Because leaves already have a value

        if isUnary:
            head, branch = span
            check = branch in self.values

        if isBinary:
            head, left, right = span
            checkLeft = left in self.values
            checkRight = right in self.values
            check = checkLeft and checkRight

        if check and isLeaf:
            self.values[leaf] = leaf[0]  # The token

        if check and isUnary:
            _, action, arg = self.actions[head[3]]  # Magic number 3
            argument = self.values[branch]
            arg = list(reversed(arg(argument).collect()))
            self.values[head] = action(*arg)

        if check and isBinary:
            _, action, args = self.actions[head[3]] # These should all be objects, not tuples
            left = self.values[left]
            right = self.values[right]
            args = args(left, right)
            args = list(reversed(args.collect()))
            self.values[head] = action(*args)

    def value(self, tokens):

        self.values = {}

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

            for s in unary[k]:
                for t in unary[k]:
                    self.setValue(t)

        begin = 0
        end = max(distances)

        fullSpans = [
            span for span in self.values if span[1] == begin and span[2] == end
        ]

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
            self.spans[index, index].add(((token, index, index, self.parser.tag(token)), ))

        while self.unvisited:
            current = self.unvisited.pop()
            label, begin, end, action = current
            self.trigger(current)

            left = set(self.endAt[begin - 1])
            for other in left:
                self.triggerPair(other, current)

            right = set(self.beginAt[end + 1])
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
        spanContent = tuple(self.tokens[begin:end + 1])
        self.readable.add((label, spanContent))

    def addToken(self, index, token):
        self.addSpan(token, index, index, TOKEN)

    def compare(self, left, right):
        leftLabel, i, j, leftName = left
        rightLabel, k, l, rightName = right
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
            spanItems = list(self.spans[indices])
            self.spans[indices] = [i for i in spanItems if not set(i) & remove]

# These are most special characters visible in a QWERTY keyboard
defaultSpecial = ('" ' + "< > ( ) { } [] / \\ ' ! = + - * & | % $ ^ ? @ # ~ ; : , . ").split()

def defaultTokenizer(string, specialCharacters=defaultSpecial):
    for p in defaultSpecial:
        string = string.replace(p, f' {p} ')
    return string.split()
    
def whitespaceTokenizer(string, specialCharacters=defaultSpecial):
    for p in defaultSpecial:
        string = string.replace(p, f' {p} ')
    string = " NEWLINE ".join(string.split(NEWLINE))
    string = " TAB ".join(string.split(TAB))
    string = " SPACE ".join(string.split(SPACE))
    return string.split()
    
inventory = lambda: defaultdict(lambda: set())

whitespaceRules = tokensToRules(['TAB', TAB], 'tab') + tokensToRules(['NEWLINE', NEWLINE], 'newline') + tokensToRules(['SPACE', SPACE], 'space')
