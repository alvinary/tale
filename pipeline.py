from collections import defaultdict
from itertools import islice as iteratorslice
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

    def __init__(self, level=0):
        self.data = defaultdict(lambda: [])
        self.level = level

    def log(self, field, data, priority):
        if priority == self.level:
            self.data[field].append(data)


defaultLogger = Log()


# When unfolding a rule with variables
class EmptySort(Exception):
    pass


# In rules
# In function declarations with let
class UndefinedSort(Exception):
    pass


# Undefined variables will always be treated as constants

# Maybe there should be some mechanism for detecting potential typos
# (Even if it's just edit distance and the message is shown only
# with a debugging flag)


# When accessing const.fun
class UndefinedFunction(Exception):
    pass


def argumentParser():
    parser = argparse.ArgumentParser(description=DESCRIPTION, epilog=EPILOG)
    parser.add_argument(
        dest='inputProgram',
        default="",
        help='The input logic program, which should be a text file.')
    parser.add_argument(
        '-n',
        dest='requestedModels',
        default=1,
        help='Number of models to show, if the input program is satisfiable.')
    parser.add_argument('-v',
                        dest='verbosityFlag',
                        default=0,
                        help='Verbosity level.')
    parser.add_argument('-p', dest='predicates', nargs="+", type=str)
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
    return {
        index.fromDimacs(literal).show()
        for literal in model if literal > 0
    }


def atomRelation(atom):
    endIndex = atom.find('(')
    return atom[0:endIndex].strip()


def printModel(model, filters=set()):
    if filters:
        model = [l for l in model if atomRelation(l) in filters]
    print("\n".join(sorted(list(model))))
    print("\n")


def showDimacs(clause, index):
    positives = [index.fromDimacs(i).show() for i in clause if i > 0]
    negatives = [
        '~ ' + index.fromDimacs(abs(i)).show() for i in clause if i < 0
    ]
    return negatives + positives


def functionClauses(index, functions):
    for f in functions.keys():
        _domain, _range = functions[f]
        _domain = [index.sortMap[d] for d in _domain]
        _range = index.sortMap[_range]
        for clause in oneOf(_range, _domain, label=f):
            yield clause


def pipeline(program, logLevel=0, logger=defaultLogger):

    logger.level = logLevel

    _sorts, _variables, _values, _functions, rules = parseProgram(program)

    for r in rules:
        logger.log(RULES, r.show(), 1)

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
                logger.log(CLAUSES, (clause, comparison.show()), 2)

    for clauseSet in functionClauses(index, _values):
        logger.log(GROUNDRULES, clauseSet.show(), 2)
        for clause in clauseSet.clausify(dimacs):
            solver.add_clause(clause)
            logger.log(CLAUSES, (clause, clauseSet.show()), 2)

    for rule in rules:
        source = rule.collect(index)
        if unfold(rule, index):
            for groundRule in unfold(rule, index):
                logger.log(GROUNDRULES, groundRule.show(), 2)
                for atom in groundRule.atoms():
                    if atom.show() not in atomForms and isPositive(atom):
                        atomForms.add(atom.show())
                        atoms.append(atom)
                        logger.log(ATOMS, atom.show(), 2)
                for clause in groundRule.clausify(dimacs):
                    solver.add_clause(clause)
                    logger.log(CLAUSES, (clause, groundRule.show()), 2)
        else:
            solver.add_clause(rule.clausify(dimacs))
            logger.log(CLAUSES, (rule.clausify(dimacs), rule.show()), 2)

    for clauseSet in negation(atoms):
        logger.log(GROUNDRULES, clauseSet.show(), 2)
        for clause in clauseSet.clausify(dimacs):
            solver.add_clause(clause)
            logger.log(CLAUSES, (clause, clauseSet.show()), 3)

    for model in solver.enum_models():
        yield showModel(model, dimacs)


if __name__ == '__main__':

    argParser = argumentParser()
    arguments = vars(argParser.parse_args())

    chatty = arguments["verbosityFlag"]
    program = arguments["inputProgram"]
    size = arguments["requestedModels"]
    included = arguments["predicates"]

    programText = ""
    with open(program) as programFile:
        for line in programFile:
            programText = f"{programText}\n{line}"

    size = int(size)
    chatty = int(chatty)
    count = 1

    if included:
        included = set(included)
    else:
        included = set()

    models = pipeline(programText, logLevel=chatty)

    if models:
        print("The input program is satisfiable.")
        print("")
        if size > 1:
            print(f"Showing up to {size} models...")
        elif size == 1:
            print(f"Showing one model...")
        print("")

    for i, m in enumerate(iteratorslice(models, size)):
        print(f"Model {i + 1}:\n")
        printModel(m, filters=included)
        print("\n\n")

    for key in defaultLogger.data.keys():
        print(key, ":")
        print("\n".join(defaultLogger.data[key]))
        print("\n\n\n")
