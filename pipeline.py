from collections import defaultdict
import argparse

from pysat.solvers import Solver

from tale.embeddings import *
from tale.formulas import *
from tale.programs import parseProgram

RULES = "r"
GROUNDRULES = "gr"
ATOMS = "a"
CLAUSES = "cl"

DESCRIPTION = '''
Find out if a logic program is satisfiable, and list some models, if any.
'''

EPILOG = 'Verbosity levels show: 1- rules, 2- grounded rules, and \n 3- dimacs ground clauses.\n'

POSITIVE_COMPARISONS = ["=", "<", "<="]

class Log:
    def __init__(self):
        self.data = defaultdict(lambda: [])

    def log(self, field, data):
        self.data[field].append(data)

logger = Log()

def argumentParser():
    parser = argparse.ArgumentParser(description=DESCRIPTION,
                                     epilog=EPILOG)
    parser.add_argument('-i', dest='inputProgram', default="",
                        help='The input logic program, which should be a text file.')
    parser.add_argument('-n', dest='requestedModels', default=1,
                        help='Number of models to show, if the input program is satisfiable.')
    parser.add_argument('-v', dest='verbosityFlag', default=0,
                        help='Verbosity level.')
    return parser

def isPositive(atom):
    if isinstance(atom, Atom):
        return isPositiveAtom(atom)
    if isinstance(atom, Comparison):
        return isPositiveComparison(atom)

def isPositiveComparison(atom):
    return atom.comparison in POSITIVE_COMPARISONS

def isPositiveAtom(atom):
    if len(atom.terms[0].term) >= 4:
        return 'not ' != atom.terms[0].term[0:4]
    else:
        return True

def showModel(model, index):
    return {index.fromDimacs(literal).show() for literal in model if literal > 0}
    
def printModel(model):
    print("\n".join(sorted(list(model))))
    print("\n")
    
def showDimacs(clause, index):
    positives = [index.fromDimacs(i).show() for i in clause if i > 0]
    negatives = ['~ ' + index.fromDimacs(abs(i)).show() for i in clause if i < 0]
    return negatives + positives

def functionClauses(index, functions):
    for f in functions.keys():
        _domain, _range = functions[f]
        _domain = [index.sortMap[d] for d in _domain]
        _range = index.sortMap[_range]
        for clause in oneOf(_range, _domain, label=f):
            yield clause

def pipeline(program, log=0):

    if log > 0:
        global logger

    _sorts, _variables, _values, _functions, rules = parseProgram(program)
    
    if log > 1:
        for r in rules:
            logger.log(RULES, r.show())
        
    index = Index(sorts=_sorts, variables=_variables, functions=_functions)
    dimacs = DimacsIndex([])
    solver = Solver()
    
    atomForms = set()
    atoms = []
    
    for sortName in index.sortMap.keys():
        sort = index.sortMap[sortName]
        for comparison in uniqueNameAssumption(sort):
            if comparison.show() not in atomForms:
                atoms.append(comparison)
                atomForms.add(comparison.show())
            for clause in comparison.clausify(dimacs):
                solver.add_clause(clause)
                logger.log(CLAUSES, clause)

    for clauseSet in functionClauses(index, _values):
        logger.log(GROUNDRULES, clauseSet.show())
        for clause in clauseSet.clausify(dimacs):
            solver.add_clause(clause)
            logger.log(CLAUSES, clause)

    for rule in rules:
        source = rule.collect(index)
        if unfold(rule, index):
            for groundRule in unfold(rule, index):
                logger.log(GROUNDRULES, groundRule.show())
                for atom in groundRule.atoms():
                    if atom.show() not in atomForms and isPositive(atom):
                        atomForms.add(atom.show())
                        atoms.append(atom)
                        logger.log(ATOMS, atom.show())
                for clause in groundRule.clausify(dimacs):
                    solver.add_clause(clause)
                    logger.log(CLAUSES, clause)
        else:
            solver.add_clause(rule.clausify(dimacs))
            logger.log(CLAUSES, rule.clausify(dimacs))

    for clauseSet in negation(atoms):
        logger.log(GROUNDRULES, clauseSet.show())
        for clause in clauseSet.clausify(dimacs):
            solver.add_clause(clause)
            logger.log(CLAUSES, clause)

    for model in solver.enum_models():
        yield showModel(model, dimacs)

if __name__ == '__main__':

    argParser = argumentParser()
    arguments = vars(argParser.parse_args())

    chatty = arguments["verbosityFlag"]
    program = arguments["inputProgram"]
    size = arguments["requestedModels"]
    
    programText = ""
    with open(program) as programFile:
        for line in programFile:
            programText = f"{programText}\n{line}"
            
    size = int(size)
    chatty = int(chatty)
    count = 1

    models = pipeline(programText, log=chatty)
            
    if models:
        print("The input program is satisfiable.")
        print("")
        if size > 1:
            print(f"Showing up to {size} models...")
        elif size == 1:
            print(f"Showing one model...")
        print("")

    for m in models:
        print(f"Model {count}:")
        printModel(m)
        print("")
        print("")
        count += 1
        if size - count < 0:
            break

    if chatty > 0:
        print("Rules: ")
        for r in logger.data[RULES]:
            print(r)
        print("")

    if chatty > 1:
        print("Ground rules: ")
        for r in logger.data[GROUNDRULES]:
            print(r)
        print("")
        
        print("Atoms: ")
        for a in logger.data[ATOMS]:
            print(a)
        print("")
        
    if chatty > 2:
        print("DIMACS clauses: ")
        for c in logger.data[CLAUSES]:
            print(c)
        print("")
        
