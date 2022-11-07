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
