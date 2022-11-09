import pytest
from tale.formulas import *
from tale.embeddings import *

a = Term('a', [])
b = Term('b', [])
p = Term('p', [])

atoms = [Atom([p, a, a]), Atom([p, b, a]), Atom([p, a, b])]

def test_negation():
    
    target = {
        'not p(a, a)',
        'not p(b, a)',
        'not p(a, b)'
    }

    for either in negation(atoms):
        assert either.options[1].show() in target

def test_oneOf():
    target = {}
    oneOf1 = oneOf(termify('A', 'B', 'C', 'D'), termify('1', '2', '3', '4'), label='letter')
    oneOf1 = sorted([r.show() for r in oneOf1])
    for s in oneOf1:
        print(s)
