from math import log, ceil

from tale.formulas import *

# Auxiliary functions and constants

IMAGE = Term('image', [])
BIT = 'bit'

def bits(n):
    return format(n, 'b')

def termify(*args):
    return [Term(a, []) for a in args]

def bitAtom(label, bit, elem):
    return Atom(termify(label, bit, elem.term))

def flip(bit):
    options = ['0', '1']
    options.remove(bit)
    return options.pop(0)

def chooseOne(p, q, a):
    return Either([Atom([p, a]), Atom([p, q])])

def imageBits(index, image, elem, label):
    allBits = []
    elemHasImage = Atom(termify('predicate', image.term, elem.term))
    for b in bits(index):
        bit = Atom(termify(label, b, elem.term))
        negatedBit = Atom(termify(label, flip(b), elem.term))
        yield Either([bit, negatedBit])
    yield Iff(allBits, [elemHasImage])

def forbid(index, elem, label=''):
    indexBits = [bitAtom(label, b, elem) for b in bits(index)]
    return Never(indexBits)

# Embeddings

def negation(atoms):
    notPrefix = 'not'
    for atom in atoms:
        terms = list(atom.terms)
        negatedPredicate = Term(f"{notPrefix} {terms[0].term}", [])
        terms = [negatedPredicate] + terms[1:]
        negatedAtom = Atom(terms)
        yield Either([atom, negatedAtom])

def unfold(rule, index):
    for assignment in index.assignments(rule.collect()):
        yield rule.evaluate(index, assignment)

def oneOf(imageSort, domainSort, label=''):

    imageSize = len(imageSort)
    bottom = 2**(ceil(log(imageSize, 2)))

    for i, image in range(imageSort):
        for elem in domainSort:
            for r in imageBits(i, image, elem, label=label):
                yield r

    for i in range(imageSize, bottom):
        for elem in domainSort:
            yield forbid(i, elem, label=label)
