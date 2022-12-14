from math import log, ceil
from itertools import product

from tale.formulas import *

# Auxiliary functions and constants

IMAGE = Term('image', [])
BIT = 'bit'


def bits(n):
    return format(n, 'b')


def termify(*args):
    for a in args:
        assert isinstance(a, str)
    return [Term(a, []) for a in args]


def bitAtom(label, index, bit, elem):
    elemTerms = [e.term for e in elem]
    return Atom(termify(label, index, bit, *elemTerms))


def flip(bit):
    options = ['0', '1']
    options.remove(bit)
    return options.pop(0)


def pad(word, length, char='0'):
    assert len(word) <= length
    return char * (length - len(word)) + word


def chooseOne(p, q, a):
    return Either([Atom([p, a]), Atom([q, a])])


def imageBits(index, image, args, label, padding):
    elementBits = []
    argumentTerms = [arg.term for arg in args]
    elemHasImage = Atom(termify(label, *argumentTerms, image.term))
    for i, b in enumerate(pad(bits(index), padding)):
        stringIndex = str(i)
        labelBit = f'{label} bit'
        bit = bitAtom(labelBit, stringIndex, b, args)
        negatedBit = bitAtom(labelBit, stringIndex, flip(b), args)
        elementBits.append(bit)
        yield Either([bit, negatedBit])
    yield Iff(elementBits, [elemHasImage])


def forbid(index, padding, args, label=''):
    indexBits = []
    argumentTerms = [elem.term for elem in args]
    for i, b in enumerate(pad(bits(index), padding)):
        indexBits.append(
            Atom(termify(f'{label} bit', str(i), b, *argumentTerms)))
    return Never(indexBits)


# Clause embeddings


def negation(atoms):
    for atom in atoms:
        yield Either([atom, atom.negate()])


def unfold(rule, index):
    for assignment in index.assignments(rule.collect(index)):
        yield rule.evaluate(index, assignment)


def oneOf(imageSort, domainSorts, label=''):

    imageSize = len(imageSort)
    logSize = ceil(log(imageSize, 2))
    bottom = 2**logSize

    for i, image in enumerate(imageSort):
        for args in product(*domainSorts):
            for r in imageBits(i, image, args, label, logSize):
                yield r

    for i in range(imageSize, bottom):
        for args in product(*domainSorts):
            yield forbid(i, logSize, args, label=label)


# Index embeddings


def totalOrder(size, prefix, sort):
    sorts = {sort: []}
    functions = {}
    for i in range(size):
        current = f"{prefix}{i}"
        _next = f"{prefix}{i+1}"
        # If next is out of bounds, it does not matter, because
        # next is not part of any sort, and should not be involved
        # in any predicate. But by adding it we ensure f(a) is always
        # defined.
        sorts[sort].append(Term(current, []))
        functions['next', current] = _next
    return sorts, {}, {}, functions


def uniqueNameAssumption(constants):
    size = len(constants)
    for i in range(size):
        for j in range(size):
            c1 = constants[i]
            c2 = constants[j]
            if c1 != c2:
                yield Comparison('!=', c1, c2)
            elif c1 == c2:
                yield Comparison('=', c1, c2)


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
