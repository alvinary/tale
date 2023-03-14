from tale.cyk import *

test_grammar = '''
    := @
    NUMBER -> DIGITS                           := x : int(x)
    NUMBER -> [LPAREN] NUMBER [RPAREN]         := x : x
    NUMBER -> NUMBER [PLUS] NUMBER             := x, y : x + y
    NUMBER -> NUMBER [MINUS] NUMBER            := x, y : x - y
    NUMBER -> NUMBER [TIMES] NUMBER @5         := x, y : x * y
    NUMBER -> [MINUS] NUMBER                   := x : -x
    LPAREN -> (                                := x : x
    RPAREN -> )                                := x : x
    DIGIT -> { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 }  := x : x
    DIGITS -> DIGIT                            := x : x
    PLUS -> +                                  := x : x
    MINUS -> -                                 := x : x
    TIMES -> *                                 := x : x
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

    assert -8 in values

    tokens = "- ( ( 5 + 4 ) + 1 )".split()
    tokens = tuple(tokens)

    values = parser.value(tokens)

    assert -10 in values

    tokens = "- 2".split()
    tokens = tuple(tokens)

    values = parser.value(tokens)

    assert -2 in values

    tokens = "2 * 6".split()
    tokens = tuple(tokens)

    values = parser.value(tokens)

    assert 12 in values

    tokens = "( 3 * 3 ) + ( 2 * ( 3 + 1 ) )".split()
    tokens = tuple(tokens)

    parse = parser.parse(tokens)
    values = parser.value(tokens)

    assert 17 in values

    tokens = " 2 + 3 * 4".split()
    tokens = tuple(tokens)
    parse = parser.parse(tokens)
    values = parser.value(tokens)

    assert 14 in values and 24 not in values and 20 not in values

    print("values: ", values)


test_grammar_to_rules()
test_cyk()
test_semantics()
