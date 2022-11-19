from pysat.solvers import Solver

from tale.embeddings import *
from tale.formulas import *
from tale.programs import parseProgram

def showModel(model, index):
    return {index.fromDimacs(literal).show() for literal in model if literal > 0}

def functionClauses(index, functions):
    for f in functions.keys():
        _domain, _range = functions[f]
        _domain = [index.sortMap[d] for d in _domain]
        _range = index.sortMap[_range]
        for clause in oneOf(_range, _domain, label=f):
            yield clause

def pipeline(program):

    _sorts, _variables, _values, _functions, rules = parseProgram(program)
    
    print("Rules: ")
    for r in rules:
        print(r.show())
    print("")    
        
    index = Index(sorts=_sorts, variables=_variables, functions=_functions)
    dimacs = DimacsIndex([])
    solver = Solver()

    for clauseSet in functionClauses(index, _values):
        for clause in clauseSet.clausify(dimacs):
            solver.add_clause(clause)

    for rule in rules:
        source = rule.collect(index)
        if unfold(rule, index):
            for groundRule in unfold(rule, index):
                for clause in groundRule.clausify(dimacs):
                    solver.add_clause(clause)
        else:
            solver.add_clause(rule.clausify(dimacs))
            
    for atom in dimacs.dimacsMap.keys():
        for clauseSet in negation():

    for model in solver.enum_models():
        yield showModel(model, dimacs)

if __name__ == '__main__':
    line = True
    program = ''

    while line:
        line = input()
        program += line

    pipeline(program)
