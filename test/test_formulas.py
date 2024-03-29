from pyclbr import Function
import pytest
from pysat.solvers import Solver
from tale.formulas import *

a = Term('a', ())
b = Term('b', ())
c = Term('c', ())
d = Term('d', ())
p = Term('p', ())
q = Term('q', ())
r = Term('r', ())
t = Term('t', ())
s = Term('s', ())

pa = Atom((p, a))
qa = Atom((q, a))
sa = Atom((s, a))
pab = Atom((p, a, b))
qab = Atom((q, a, b))
rba = Atom((r, b, a))
pb = Atom((p, b))
sab = Atom((s, a, b))
ta = Atom((t, a))

def test_terms():

    # Define constants, functions, and a variable 'v',
    # which ranges over functions

    funs = ("f", "g")
    cons = (a, b, c, d)

    vals = {
        ('f', 'a'): 'a',
        ('f', 'b'): 'a',
        ('f', 'c'): 'd',
        ('f', 'd'): 'c',
        ('g', 'a'): 'b',
        ('g', 'b'): 'a',
        ('g', 'c'): 'd',
        ('g', 'd'): 'c'
    }

    assign = Assignment({'v': 'g'})
    varbs = {'v': 'funs'}

    # 1a) Test a single term with a single function, f(a)
    # 1b) Test a compund term, g(f(a))

    index = Index(functions=vals, variables=varbs)
    term1 = Term('a', functions=('f',))
    term2 = Term('a', functions=('f', 'g'))

    val_1a = term1.evaluate(index, assign)
    val_1b = term2.evaluate(index, assign)

    assert val_1a == a

    assert val_1b == b

    # Test with assignment
    term3 = Term('a', functions=('f', 'g', 'v'))
    val2 = term3.evaluate(index, assign)

    assert val2 == a

    # Test error

    term4 = Term("gggg", ("f",))
    try:
        val = term4.evaluate(index, assign)
    except FunctionError:
        assert True


def test_rules():

    rule1s = "p(a, b) -> q(a)"
    rule2s = "q(a, b), p(a, b) -> False"
    rule3s = "p(a), r(b, a), p(b) <-> s(a, b)"
    rule4s = "Either q(a), s(a)"
    rule5s = "t(a) v p(a) v q(a)"

    a = Term('a', ())
    b = Term('b', ())
    p = Term('p', ())
    q = Term('q', ())
    r = Term('r', ())
    t = Term('t', ())
    s = Term('s', ())

    rule1 = If((pab,), (qa,))
    rule2 = Never((qab, pab))
    rule3 = Iff((pa, rba, pb), (sab,))
    rule4 = Either((qa, sa))
    rule5 = Or((ta, pa, qa))

    assert rule1.show() == rule1s
    assert rule2.show() == rule2s
    assert rule3.show() == rule3s
    assert rule4.show() == rule4s
    assert rule5.show() == rule5s


def test_assigments():

    testSorts = {
        's': ['a', 'b'],
        't': ['c', 'd'],
        'v': ['f', 'g'],
        'r': ['s', 't']
    }

    testVariables = {'v': 'v', 'r': 'r', 'x': 's'}

    testIndex = Index(sorts=testSorts, variables=testVariables)

    target = {('a', 'f'), ('b', 'f'), ('a', 'g'), ('b', 'g')}
    bindings = testIndex.assignments(['x', 'v'])
    covered = {(b.binding['x'], b.binding['v']) for b in bindings}
    assert target == covered


def test_embedding():

    solver = Solver()

    dimacs = DimacsIndex(atoms=[pa, qa, pab, qab, rba, pb, sab, ta])

    iff1 = Iff((pa,), (qa,))
    if1 = If((ta,), (pb,))
    either1 = Either((ta, qa))
    or1 = Or((ta, qa, pa, pb, sab))
    never1 = Never((sab, qa))

    rules = [iff1, if1, either1]

    for rule in rules:
        for clause in rule.clausify(dimacs):
            print("add: ", clause)
            solver.add_clause(clause)

    iffAtoms = {pa.show(), qa.show()}

    cond1 = lambda m: not (m & iffAtoms) or iffAtoms <= m
    cond2 = lambda m: ta.show() not in m or pb.show() in m
    cond3 = lambda m: not (ta.show() in m and qa.show() in m)
    cond4 = lambda m: ta.show() in m or qa.show() in m or pa.show(
    ) in m or pb - show() in m or sab.show() in m
    cond5 = lambda m: not (sab.show() in m and qa.show() in m)

    readable = lambda m: {
        dimacs.fromDimacs(a).show()
        for a in m if a > 0 and isinstance(a, int)
    }

    listedModels = 0

    solver.solve()

    for m in solver.enum_models():
        print(m)
        m = readable(m)
        print(m)
        assert cond1(m)
        assert cond2(m)
        assert cond3(m)
        listedModels += 1

    assert listedModels != 0
