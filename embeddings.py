from math import log, ceil
from itertools import product

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

def pad(word, length, char='0'):
    return char * (length - len(word)) + word

def chooseOne(p, q, a):
    return Either([Atom([p, a]), Atom([p, q])])

def imageBits(index, image, args, label, padding):
    allBits = []
    argumentTerms = [elem.term for elem in args]
    elemHasImage = Atom(termify('predicate', image.term, *argumentTerms))
    for i, b in enumerate(pad(bits(index), padding)):
        stringIndex = str(i)
        bit = Atom(termify(label, stringIndex, b, *argumentTerms))
        negatedBit = Atom(termify(label, stringIndex, flip(b), *argumentTerms))
        allBits.append(bit)
        yield Either([bit, negatedBit])
    yield Iff(allBits, [elemHasImage])

def forbid(index, elem, label=''):
    indexBits = [bitAtom(label, b, elem) for b in bits(index)]
    return Never(indexBits)

# Clause embeddings

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

def oneOf(imageSort, domainSorts, label=''):

    imageSize = len(imageSort)
    logSize = (ceil(log(imageSize, 2)))
    bottom = 2**logSize

    for i, image in enumerate(imageSort):
        for args in product(*domainSorts):
            for r in imageBits(i, image, args, label, logSize):
                yield r

    for i in range(imageSize, bottom):
        for elem in domainSort:
            yield forbid(i, elem, label=label)

# Index embeddings

def totalOrder(size, prefix, sort):
    sorts = {sort : []}
    functions = {}
    for i in range(size):
        current = f"{prefix}{i}"
        _next = f"{prefix}{i+1}"
        # If next is out of bounds, it does not matter, because
        # next is not part of any sort, and should not be involved
        # in any predicate. But by adding it we ensure f(a) is always
        # defined.
        sorts[sort].append(current)
        values['next', current] = _next
    return sorts, {}, {}, functions

# Mixed embeddings

def binaryTree(size, label=''):
    
    leaves = []
    partMap = {}

    partMap['left'] = []
    partMap['right'] = []

    # virtual or actual
    # virtuals have a direction
    # inherit in that direction directly
    # show


