from collections import defaultdict

index = lambda: defaultdict(lambda: [])

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
    endsAt = index()
    beginsAt = index()

    spans = set()

    tokenLabels = [tokenizer(elem) for elem in sequence]
    # This might require a function argument to be more general

    for index, token in enumerate(tokens):
        tokenSpan = (index, index, label, TOKEN)
        endsAt[index].append(tokenSpan)
        beginsAt[index].append(tokenSpan)

    while notVisited:

        currentSpan = notVisited.pop()

        rightBegin = leftEnd + 1
        leftEnd = spanBegin - 1

        leftBegin, leftEnd, leftLabel, leftRule = currentSpan
        candidates = beginsAt[rightBegin]

        # (1) Why not have rulesByLeft and rulesByRight?
        for candidate in candidates:
            rightBegin, rightEnd, rightLabel, rightRule = candidate
            production = (leftLabel, rightLabel)
            for newLabel, newRule in ruleTriggers[production]:
                # This (ruleTriggers[production]) can be empty, so no need for (1)
                newSpan = (leftBegin, rightEnd, newLabel, newRule)
                beginsAt[newBegin].append(newSpan)
                endsAt[newEnd].append(newSpan)
                notVisited.add(newSpan)
                spans.add(newSpan)

                # But there is duplicate code below, which would
                # not be necessary with 'productions by direction'

        rightBegin, rightEnd, rightLabel, rightRule = currentSpan
        candidates = endsAt[leftEnd]

        for candidate in candidates:
            leftBegin, leftEnd, leftLabel, leftRule = candidate
            production = (leftLabel, rightLabel)
            for newLabel, newRule in ruleTriggers[production]:
                newSpan = (leftBegin, rightEnd, newLabel, newRule)
                beginsAt[newBegin].append(newSpan)
                endsAt[newEnd].append(newSpan)
                notVisited.add(newSpan)
                spans.add(newSpan)

    return spans


