from formulas import *

def negation(atoms):
    notPrefix = 'not'
    for atom in atoms:
        terms = list(atom.terms)
        terms[0] = f"{notPrefix} {terms[0]}"
        negatedAtom = Atom(terms)
        yield Either([atom, negatedAtom])

