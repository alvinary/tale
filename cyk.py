from collections import defaultdict

index = lambda: defaultdict(lambda: [])

PUNCTUATION = set(";->!=(),<")

def isPunctuation(character):
    return character in PUNCTUATION

def tokenize(text):
    tokens = []
    return tokens

def tokenLabels(tokens):
    labels = []
    return labels

def cyk(tokens):

    visited = set()
    notVisited = set()
    endsAt = index()
    beginsAt = index()

    tokenLabels = labelTokens(tokens)

    for index, token in enumerate(tokens):
        for label in tokenLabels[token]:
            endsAt[index].append((index, index, label, TOKEN))

    while notVisited:

        leftBegin, leftEnd, leftLabel = notVisited.pop()
        rightBegin = leftEnd + 1
        candidates = beginsAt[rightBegin]

        for candidate in candidates:
            rightBegin, rightEnd, rightLabel = candidate
            production = (leftLabel, rightLabel)
            for newLabel, newRule in ruleTriggers[production]:
                newSpan = (leftBegin, rightEnd, newLabel, newRule)
                beginsAt[newBegin].append(newSpan)
                endsAt[newEnd].append(newSpan)
                notVisited.add(newSpan)

