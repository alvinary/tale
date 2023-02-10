from tale.cyk import *

test_grammar = '''
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
    DIGIT -> 6                           (Decimal digit)
    DIGIT -> 7                           (Decimal digit)
    DIGIT -> 8                           (Decimal digit)
    DIGIT -> 9                           (Decimal digit)
    DIGITS -> DIGIT                      (Single digit)
    DIGITS -> DIGIT DIGITS               (Several digits)
    PLUS -> +                            (Plus symbol)
    MINUS -> -                           (Minus symbol)
    TIMES -> *                           (Times symbol)
'''

identity = lambda x: x

test_triggers = {
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
    
    parse = Parser(test_grammar, test_triggers).parse(tokens)

    for span in parse.spans:
        print(parse.spans[span])
        
def test_grammar_to_rules():
    print('\nRules:\n')
    rules = textToRules(testGrammar)
    for rule in rules:
        print(rule)
    print("")
    
def test_semantics():

    parser = Parser(test_grammar, test_triggers)
    
    for r in parser.grammar:
        print("Rule:", r, ":", grammar[r])
        
    print("")
        
    for a in parser.actions:
        print("Action:", a, ":", actions[a])
        
    print("")

test_grammar_to_rules()    
test_cyk()
test_semantics()