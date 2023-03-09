from tale.cyk import *

test_grammar = '''
    := @
    NUMBER -> DIGITS                           := x : int(x)
    NUMBER -> [LPAREN] NUMBER [RPAREN]         := x : x
    NUMBER -> NUMBER [PLUS] NUMBER             := x, y : x + y
    NUMBER -> NUMBER [MINUS] NUMBER            := x, y : x - y
    NUMBER -> [MINUS] NUMBER                   := x : -x
    NUMBER -> NUMBER [TIMES] NUMBER @5         := x, y : x * x
    LPAREN -> (                                := x : x
    RPAREN -> )                                := x : x
    DIGIT -> { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 }  := x : x
    DIGITS -> DIGIT                            := x : x
    DIGITS -> DIGIT DIGITS                     := x, y : x + y
    PLUS -> +                                  := x : x
    MINUS -> -                                 := x : x
    TIMES -> *                                 := x : x
'''

identity = lambda x: x

test_grammar_triggers = {
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

def test_cyk():

    tokens = "- ( 5 + 4 ) + 1".split()
    tokens = tuple(tokens)
    
    parse = Parser(test_grammar).parse(tokens)

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

    parser = Parser(test_grammar)
    
    for r in parser.grammar:
        print("Rule:", r, ":", parser.grammar[r])
        
    print("")
        
    for a in parser.actions:
        print("Action:", a, ":", parser.actions[a])

def test_value():

    tokens = "( - ( 5 + 4 ) ) + 1".split()
    tokens = tuple(tokens)
    
    parser = Parser(test_grammar)
    values = parser.value(tokens)
    
    assert -8 in values
    
    tokens = "- ( ( 5 + 4 ) + 1 )".split()
    tokens = tuple(tokens)
    
    parser = Parser(test_grammar)
    values = parser.value(tokens)
    
    assert -10 in values

    tokens = "- 2".split()
    tokens = tuple(tokens)
    
    parser = Parser(test_grammar)
    values = parser.value(tokens)
    
    assert -2 in values

    tokens = "( 1 + 1 * 3 ) + 6 * 3".split()
    tokens = tuple(tokens)
    
    parser = Parser(test_grammar)
    parse = parser.parse(tokens)
    for indices in parse.spans:
        print(indices)
        for span in parse.spans[indices]:
            print(span)

    values = parser.value(tokens)
    
    assert 22 in values and 30 not in values

    tokens = "2 * 3".split()
    tokens = tuple(tokens)
    
    parser = Parser(test_grammar)
    values = parser.value(tokens)
    
    assert 6 in values
 

test_grammar_to_rules()    
test_cyk()
test_semantics()
