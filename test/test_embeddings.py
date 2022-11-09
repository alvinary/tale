import pytest
from tale.formulas import *
from tale.embeddings import *
from pysat.solvers import Solver

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
    rules = list(oneOf(termify('A', 'B', 'C', 'D'), termify('1', '2', '3', '4'), label='letter'))
    ruleStrings = sorted([r.show() for r in rules])

    for s in ruleStrings:
        print(s)

    solver = Solver()
    dimacs = DimacsIndex([])
    clauses = []

    for r in rules:
        dimacs.addRule(r)
        clauses += list(r.clausify(dimacs))

    for c in clauses:
        solver.add_clause(c)
    
    count = 0
    for m in solver.enum_models():
        count += 1

    assert count == 256
