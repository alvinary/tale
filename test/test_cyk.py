from tale.cyk import *
from math import floor

test_grammar = '''
    := @
    NUMBER -> INTEGER                          := x : int(x)
    NUMBER -> FLOAT                            := x : float(x)
    INTEGER -> DIGITS @15                      := x : x
    FLOAT -> DIGITS [DOT] DIGITS @20           := x, y : x + '.' + y
    NUMBER -> [LPAREN] NUMBER [RPAREN]         := x : x
    NUMBER -> NUMBER [PLUS] NUMBER             := x, y : x + y
    NUMBER -> NUMBER [MINUS] NUMBER            := x, y : x - y
    NUMBER -> NUMBER [TIMES] NUMBER @5         := x, y : x * y
    NUMBER -> [MINUS] NUMBER                   := x : -x
    NUMBER -> NUMBER [POWER] NUMBER            := x, y : x ** y
    NUMBER -> NUMBER [BETWEEN] NUMBER          := x, y : x / y
    LPAREN -> (                                := x : x
    RPAREN -> )                                := x : x
    DIGIT -> { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 }  := x : x
    DIGITS -> DIGIT                            := x : x
    DIGITS -> DIGIT DIGITS                     := x, y : x + y
    PLUS -> +                                  := x : x
    MINUS -> -                                 := x : x
    TIMES -> *                                 := x : x
    POWER -> ^                                 := x : x
    BETWEEN -> /                               := x : x
    DOT -> .                                   := x : x
    COMMA -> ,                                 := x : x
    LSQUARE -> [                               := x : x
    RSQUARE -> ]                               := x : x
    LIST -> [LSQUARE] ELEMS [RSQUARE]          := x : x
    ELEMS -> NUMBER                            := x : x
    ELEMS -> NUMBER [COMMA] ELEMS              := x, xs : xs.append(x)
'''

identity = lambda x: x

test_grammar_triggers = {
    '5': [("NUMBER", "Single digit")],
    '4': [("NUMBER", "Single digit")],
    '1': [("NUMBER", "Single digit")],
    '(': [("LPAREN", "( symbol")],
    ')': [("RPAREN", ") symbol")],
    '+': [("PLUS", "+ symbol")],
    '-': [("MINUS", "- symbol")],
    '^': [("POWER", "+ symbol")],
    '*': [("TIMES", "- symbol")],
    '/': [("TIMES", "- symbol")],
    ('PLUS', 'NUMBER'): [("PLUSNUMBER", "Addition")],
    ('MINUS', 'NUMBER'): [("NUMBER", "Additive inverse")],
    ('NUMBER', 'PLUSNUMBER'): [("NUMBER", "Sum")],
    ('LPAREN', 'PARENNUMBER'): [("NUMBER", "Closing parentheses")],
    ('NUMBER', 'RPAREN'): [("PARENNUMBER", "Opening parentheses")]
}


def test_cyk():

    tokens = "- ( 5 + 4 ) + 1".split()
    tokens = tuple(tokens)

    parse = parserFromGrammar(test_grammar).parse(tokens)

    for span in parse.readable:
        print('span:', span)

    assert ('NUMBER', tokens) in parse.readable
    assert ('NUMBER', tokens[7:]) in parse.readable
    assert ('NUMBER', tokens[1:6]) in parse.readable


def test_grammar_to_rules():
    print('\nRules:\n')
    sep, prec, lines = getLines(test_grammar)
    rules = linesToRules(lines, sep, prec)
    for rule in rules:
        print(rule)
    print("")


def test_semantics():

    parser = parserFromGrammar(test_grammar)

    for r in parser.grammar:
        print("Rule:", r, ":", parser.grammar[r])

    print("")

    for a in parser.actions:
        print("Action:", a, ":", parser.actions[a])


def test_value():

    tokens = "( - ( 5 + 4 ) ) + 1".split()
    tokens = tuple(tokens)

    parser = parserFromGrammar(test_grammar)
    parser.actions['TOKEN'] = lambda x: x
    for a in parser.actions:
        print("Action:", a, ":", parser.actions[a])

    values = parser.value(tokens)

    print(values)
    assert -8 in values

    tokens = "- ( ( 5 + 4 ) + 1 )".split()
    tokens = tuple(tokens)

    values = parser.value(tokens)

    print(values)
    assert -10 in values

    tokens = "- 2".split()
    tokens = tuple(tokens)

    values = parser.value(tokens)

    print(values)
    assert -2 in values

    tokens = "2 * 6".split()
    tokens = tuple(tokens)

    values = parser.value(tokens)

    print(values)
    assert 12 in values

    tokens = "( 3 * 3 ) + ( 2 * ( 3 + 1 ) )".split()
    tokens = tuple(tokens)

    parse = parser.parse(tokens)
    values = parser.value(tokens)

    print(values)
    assert 17 in values

    tokens = " 2 + 3 * 4".split()
    tokens = tuple(tokens)
    parse = parser.parse(tokens)
    values = parser.value(tokens)

    print(values)
    assert 14 in values and 24 not in values and 20 not in values

    tokens = "2 + 4 * 5 + 6".split()
    tokens = tuple(tokens)
    parse = parser.parse(tokens)
    values = parser.value(tokens)
    
    print(values)
    assert 28 in values
    
    expr = tuple([c for c in '((((2*4)-(7*3))+((4*1)-(5*5)))/(((7/6)-(7/8))+((9/8)-(4^2))))*((((7^3)-(1/4))+((5/5)-(6/7)))/(((8/7)-(8/9))+((4)-(7))))+((((2*4)-(7*3))+((4*1)-(5*5)))/(((7/6)-(7/8))+((9/8)-(4^2))))*((((7^3)-(1/4))+((5/5)-(6/7)))/(((8/7)-(8/9))+((4)-(7))))'])
    
    values = parser.value(expr)
    
    print(values)
    assert -583 in [floor(v) for v in values]
    assert len(values) == 1
    
    expr = tuple([c for c in '(((((211275*4)-(7*3))+((4*1)-(51213*5)))/(((7/6)-(7/8))+((9/8)-(4^2))))*((((7^3)-(1/4))+((5/5)-(6/7)))/(((8/7)-(8.2/9))+((422)-(73))))+((((2.4*4)-(755*3))+((4*1)-(5*5)))/(((7/6)-(7/8))+((9/8)-(4^2))))*((((7^3)-(1/4))+((5/5)-(6/7)))/(((8/7)-(81/9))+((4)-(7)))))'])
    
    values = parser.value(expr)
    
    print(values)
    assert -44587 in [floor(v) for v in values]
    assert len(values) == 1


test_grammar_to_rules()
test_cyk()
test_semantics()
