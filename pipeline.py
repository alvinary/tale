from pysat.solvers import Solver

from tale.embeddings import *
from tale.formulas import *
from tale.programs import parseProgram

def showModel(model, index):
    return {index.fromDimacs(literal).show() for literal in model}

def functionClauses(index, functions):
    for f in functions.keys():
        _domain, _range = functions[f]
        _domain = [index.sortMap[d] for d in _domain]
        _range = index.sortMap[_range]
        for clause in oneOf(_range, _domain, label=f):
            yield clause

def pipeline(program):

    _variables, _sorts, functions, rules = parseProgram(program)

    index = Index(sorts=_sorts, variables=_variables)
    dimacs = DimacsIndex()
    solver = Solver()

    for clause in functionClauses(index, functions):
        solver.add_clause(clause.clausify(dimacs))

    for rule in rules:
        source = rule.collect(index)
        for assignment in index.assignments(source):
            solver.add_clause(rule.evaluate(index, assignment).clausify(index))

    for model in solver.enum_models():
        yield showModel(model)

if __name__ == '__main__':
    line = True
    program = ''

    while line:
        line = input()
        program += line

    pipeline(program)
