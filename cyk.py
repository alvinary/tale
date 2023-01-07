from collections import defaultdict

inventory = lambda : defaultdict(lambda : set())

PUNCTUATION = set(";->!=(),<")
IDENTITY = lambda x: x
TOKEN = 'token label'

def isPunctuation(character):
    return character in PUNCTUATION

# Write a function that turns grammars with rules
# whose right hand side has more than two preterminals
# (currying rules with more than two productions),
# since it's horrible to write grammars with only
# binary rules

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

    oldSpans = set()

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
                # what if something you just added to unvisited could have some
                # other preterminal? You should do this same loop whenever you
                # add something

        candidates = set(beginsAt[leftEnd + 1])

        # (1) Why not have rulesByLeft and rulesByRight?
        for candidate in candidates:
            rightBegin, rightEnd, rightLabel, rightRule = candidate
            production = (leftLabel, rightLabel)
            if production in ruleTriggers.keys():
                for newLabel, newRule in ruleTriggers[production]:
                # This (ruleTriggers[production]) can be empty, so no need for (1)
                    newSpan = (leftBegin, rightEnd, newLabel, newRule)
                    beginsAt[leftBegin].add(newSpan)
                    endsAt[rightEnd].add(newSpan)
                    notVisited.add(newSpan)
                    spans.add((newLabel, " ".join(sequence[leftBegin:rightEnd+1])))

                # But there is duplicate code below, which would
                # not be necessary with 'productions by direction'

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

        newSpans = set(spans - oldSpans)
        oldSpans = set(spans)

        print("SPANS:")
        for s, p in newSpans:
            print(s, p)
        print("Unvisited:")
        for s in notVisited:
            print(s)
        print("\n\n")

        for k in endsAt.keys():
            print(k, " ".join([str(t) for t in endsAt[k]]))
        for k in beginsAt.keys():
            print(k, " ".join([str(t) for t in endsAt[k]]))

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

testCYK()
