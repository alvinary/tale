from collections import defaultdict
from multiprocessing import cpu_count, Pool
from itertools import islice as iteratorslice
from itertools import chain
import argparse

from pysat.solvers import Solver

from tale.embeddings import *
from tale.formulas import *
from tale.programs import parseProgram

RULES = "rules"
GROUNDRULES = "ground"
ATOMS = "atoms"
CLAUSES = "clauses"
STATS = "stats"

CHUNKSIZE = 1024

DESCRIPTION = '''
Find out if a logic program is satisfiable, and list some models, if any.
'''

EPILOG = 'Verbosity levels show: 1- rules, 2- grounded rules, and \n 3- dimacs ground clauses.\n'

POSITIVE_COMPARISONS = ["=", "<", "<="]

class Log:

    def __init__(self):
        self.data = defaultdict(lambda: [])
        self.flags = set()

    def log(self, field, data):
        if field in self.flags:
            self.data[field].append(data)


# When unfolding a rule with variables
class EmptySort(Exception):
    pass


# In rules
# In function declarations with let
class UndefinedSort(Exception):
    pass


# Terms that are not declared as variables are always treated as constants

# When accessing const.fun
class UndefinedFunction(Exception):
    pass

def emptySet():
    return set([])

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
    parser.add_argument(
        '-p',
        dest='predicates',
        nargs="+",
        type=str,
        help=
        'Names of predicates to be shown in output. If none are provied, all predicates are shown.'
    )
    parser.add_argument(
        '-l',
        dest='log',
        nargs="+",
        type=str,
        help=
        'Choose any subset of the flags { rules, ground, atoms, clauses, stats } to decide what the logger logs and then shows.'
    )
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

class Program:

    def __init__(self,
                 program_text,
                 defaultFunctions=emptySet(),
                 defaultSorts=emptySet(),
                 flags=emptySet()):
                 
        sorts, variables, values, functions, rules = parseProgram(program_text)
        functions |= defaultFunctions
        for s in defaultSorts:
            sorts[s] += defaultSorts[s]

        self.rules = rules
        self.index = Index(sorts=sorts, variables=variables, functions=functions)
        self.dimacs = DimacsIndex([])
        self.solver = Solver()
        self.logger = Log()
        self.logger.flags |= flags
        self.ready = False
        self.values = values

    def setup(self):
        
        self.index.addProjections()

        atomForms = set()
        atoms = []

        for r in self.rules:
            self.logger.log(RULES, r.show())

        for sort in self.index.sortMap.keys():
            elements = self.index.sortMap[sort]
            for comparison in uniqueNameAssumption(elements):
                if comparison.show() not in atomForms:
                    atoms.append(comparison)
                    atomForms.add(comparison.show())
                for clause in comparison.clausify(self.dimacs):
                    self.solver.add_clause(clause)
                    self.logger.log(CLAUSES, (clause, comparison.show()))

        for clauseSet in functionClauses(self.index, self.values):
            self.logger.log(GROUNDRULES, clauseSet.show())
            for clause in clauseSet.clausify(self.dimacs):
                self.solver.add_clause(clause)
                self.logger.log(CLAUSES, (clause, clauseSet.show()))

        for rule in self.rules:
            source = rule.collect(self.index)
            if unfold(rule, self.index):
                for groundRule in unfold(rule, self.index):
                    self.logger.log(GROUNDRULES, groundRule.show())
                    for atom in groundRule.atoms():
                        if atom.show() not in atomForms and isPositive(atom):
                            atomForms.add(atom.show())
                            atoms.append(atom)
                            self.logger.log(ATOMS, atom.show())
                    for clause in groundRule.clausify(self.dimacs):
                        self.solver.add_clause(clause)
                        self.logger.log(CLAUSES, (clause, groundRule.show()))
            else:
                self.solver.add_clause(rule.clausify(self.dimacs))
                self.logger.log(CLAUSES, (rule.clausify(self.dimacs), rule.show()))

        for clauseSet in negation(atoms):
            self.logger.log(GROUNDRULES, clauseSet.show())
            for clause in clauseSet.clausify(self.dimacs):
                self.solver.add_clause(clause)
                self.logger.log(CLAUSES, (clause, clauseSet.show()))

        self.ready = True

    def models(self):
        if not self.ready:
            self.setup()
        for model in self.solver.enum_models():
            self.logger.log(STATS, str(self.solver.accum_stats()))
            yield showModel(model, self.dimacs)

if __name__ == '__main__':

    argParser = argumentParser()
    arguments = vars(argParser.parse_args())

    program = arguments["inputProgram"]
    size = arguments["requestedModels"]
    included = arguments["predicates"]
    flags = arguments["log"]

    if not flags:
        flags = set()

    programText = ""
    with open(program) as programFile:
        for line in programFile:
            programText = f"{programText}\n{line}"

    size = int(size)
    count = 1

    if included:
        included = set(included)
    else:
        included = set()

    program = Program(programText, flags=flags)

    models = program.models()

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

    for key in program.logger.data.keys():
        print(key, ":")
        print("\n".join(program.logger.data[key]))
        print("\n\n\n")
