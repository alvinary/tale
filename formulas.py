from collections import defaultdict
from dataclasses import dataclass
from itertools import product
from typing import List
from functools import reduce

PROJECTION = 0

union = lambda x, y: x | y

swappedComparisons = {
            '='  : '!=',
            '!=' : '=',
            '<=' : '</=',
            '</=' : '<=',
            '<' : '</',
            '</' : '<'
            }

def reverseComparison(comparison):
    '''
    Input a string representing a comparison operator and 
    return its negation
    '''

    # Since the list of comparison operators is fixed,
    # this should be an enumeration.

    return swappedComparisons[comparison]


def isNegative(term):
    '''
    Input a Term object, and return True if its term
    attribute starts with 'not '
    '''

    # This is not very clean

    if 'not ' in term.term:
        return term.term[0:5] == 'not '
    else:
        return False


def reverseNot(term):
    '''
    Input a term object, and return another term object
    representing its negation
    '''
    if isNegative(term):
        positiveTerm = term.term[4:]
        return Term(positiveTerm, term.functions)
    else:
        return Term(f'not {term.term}', term.functions)


# Maybe we should have two separate classes
# (predicate terms and non-predicate terms)


class Ok(Exception):

    def __init__(self):
        super().__init__("")

    def __str__(self):
        return "No error."

    def __bool__(self):
        return False


class ExtensionError(Exception):

    def __init__(self, sort):
        self.sort = sort

    def __str__(self):
        return f"There is no extension for sort {self.sort}"

    def __bool__(self):
        return True


class FunctionError(Exception):

    def __init__(self, function, term):
        super().__init__("")
        self.function = function
        self.term = term

    def __str__(self):
        return f"No value found for {self.term}.{self.function}"

    def __bool__(self):
        return True


class AssignmentError(Exception):

    def __init__(self, term):
        super().__init__()
        self.term = term

    def __str__(self):
        return f"Term {self.term} has no bound value."

    def __bool__(self):
        return True


class Assignment:

    def __init__(self, mapping):
        self.binding = mapping

    # It is confusing to use the identifier 'term' here,
    # since these are strings and not Terms

    def bind(self, term):
        if term in self.binding.keys():
            return self.binding[term], Ok()
        else:
            return None, AssignmentError(term)


class DimacsIndex:

    def __init__(self, atoms):
        self.dimacsMap = {}
        self.stringMap = {}
        self.counter = 1

        for atom in atoms:
            self.addAtom(atom)

    def toDimacs(self, atom):
        return self.dimacsMap[atom.show()]

    def fromDimacs(self, dimacs):
        return self.stringMap[dimacs]

    def addAtom(self, atom):
        if atom.show() not in self.dimacsMap.keys():
            while self.counter in self.stringMap.keys():
                self.counter += 1
            dimacs_atom = self.counter
            self.dimacsMap[atom.show()] = dimacs_atom
            self.stringMap[dimacs_atom] = atom
            self.counter += 1

    def getLiteral(self, atom):
        if atom.show() in self.dimacsMap.keys():
            return self.toDimacs(atom)
        else:
            self.addAtom(atom)
            return self.toDimacs(atom)


class Index:

    def __init__(self, sorts={}, variables={}, functions={}):

        self.functionMap = {k:v for k, v in functions.items() if len(k) == 2}
        self.sortMap = sorts
        self.variableMap = variables
        self.projections = {k:v for k, v in functions.items() if len(k) == 3}

    def value(self, function, elem):

        if (function, elem) in self.functionMap.keys():
            value = self.functionMap[function, elem]
            error = Ok()
        else:
            value = None
            error = FunctionError(function, elem)

        if not isinstance(error, FunctionError):
            return value, error

        else:
            raise error

    def hasVariable(self, name):
        return name in self.variableMap.keys()

    def extension(self, sort, local_sorts={}):

        in_map = sort in self.sortMap.keys()
        in_local = sort in local_sorts.keys()

        if not in_map and not in_local:
            raise ExtensionError(sort)

        if local_sorts and sort in local_sorts.keys():
            for elem in local_sorts[sort]:
                yield elem

        if not local_sorts and in_map:
            for elem in self.sortMap[sort]:
                yield elem

    def assignments(self, variables):
        sorts = [self.variableMap[v] for v in variables]
        for assignment in product(*[self.sortMap[s] for s in sorts]):
            binding = dict(zip(variables, assignment))
            yield Assignment(binding)
            
    def addProjections(self):
        for k, v in self.projections.items():
            _, domain, function = k
            image = v
            for preimage in self.sortMap[domain]:
                imageName = f"{preimage.term}.{function}"
                imageTerm = Term(imageName, [])
                self.sortMap[image].append(imageTerm)
                self.functionMap[function, preimage.term] = imageName


@dataclass(frozen=True)
class Term:
    term: str
    functions: tuple[str]

    def evaluate(self, index, assignment):

        if index.hasVariable(self.term):
            groundTerm, error = assignment.bind(self.term)

        else:
            groundTerm = self

        groundFunctions = []

        for f in self.functions:
            if index.hasVariable(f):
                boundFunction, error = assignment.bind(f)
                groundFunctions.append(boundFunction)
            else:
                groundFunctions.append(f)

        argument = groundTerm

        if not groundFunctions:
            return argument

        while groundFunctions:

            function = groundFunctions.pop(0)

            if index.hasVariable(function):
                function, error = assignment.bind(function)
                if not isinstance(error, Ok):
                    raise error

            value, error = index.value(
                function,
                argument.term)  # What if function is a term? Can that happen?
            value = Term(value, ())

            if not isinstance(error, Ok):
                raise error

            argument = value

        return argument

    def collect(self, index):
        names = [self.term] + self.functions
        return {n for n in names if index.hasVariable(n)}

    def show(self):
        return f"{self.term}{''.join(['.' + f for f in self.functions])}"


@dataclass(frozen=True)
class Atom:
    terms: List[Term]

    def atoms(self):
        yield self

    def clausify(self, index):
        return [[index.getLiteral(self)]]

    def evaluate(self, index, assignment):
        return Atom([t.evaluate(index, assignment)] for t in self.terms)

    def collect(self, index):
        variables = set()
        for t in self.terms:
            variables |= t.collect(index)
        return variables

    def negate(self):
        return Atom([reverseNot(self.terms[0])] + self.terms[1:])

    def show(self):
        predicate = self.terms[0].show()
        arguments = [a.show() for a in self.terms[1:]]
        return f"{predicate}({', '.join(arguments)})"

    def evaluate(self, index, assignment):
        return Atom([t.evaluate(index, assignment) for t in self.terms])


@dataclass(frozen=True)
class Comparison:
    comparison: str
    left: Term
    right: Term

    def atoms(self):
        yield self

    def clausify(self, index):
        return [[index.getLiteral(self)]]

    def negate(self):
        return Comparison(reverseComparison(self.comparison), self.left,
                          self.right)

    def collect(self, index):
        variables = set()
        variables |= self.left.collect(index)
        variables |= self.right.collect(index)
        return variables

    def show(self):
        return f"{self.left.show()} {self.comparison} {self.right.show()}"

    def evaluate(self, index, assignment):
        return Comparison(self.comparison,
                          self.left.evaluate(index, assignment),
                          self.right.evaluate(index, assignment))


@dataclass(frozen=True)
class Either:
    options: List[Atom]

    def atoms(self):
        for a in self.options:
            yield a

    def clausify(self, index):
        return [[index.getLiteral(o) for o in self.options]] + [[
            -index.getLiteral(o1), -index.getLiteral(o2)
        ] for o1, o2 in product(self.options, self.options) if o1 != o2]

    def collect(self, index):
        return reduce(union, [o.collect(index) for o in self.options], set())

    def show(self):
        return f"Either {', '.join([a.show() for a in self.options])}"

    def evaluate(self, index, assignment):
        return Either([o.evaluate(index, assignment) for o in self.options])


@dataclass(frozen=True)
class If:
    body: List[Atom]
    head: List[Atom]

    def atoms(self):
        for a in self.body:
            yield a
        for a in self.head:
            yield a

    def clausify(self, index):
        return [[-index.getLiteral(a)
                 for a in self.body] + [index.getLiteral(h)]
                for h in self.head]

    def collect(self, index):
        variables = set()
        for a in self.body:
            variables |= a.collect(index)
        for a in self.head:
            variables |= a.collect(index)
        return variables

    def show(self):
        body = ', '.join([a.show() for a in self.body])
        head = ', '.join([a.show() for a in self.head])
        return f"{body} -> {head}"

    def evaluate(self, index, assignment):
        return If([b.evaluate(index, assignment) for b in self.body],
                  [h.evaluate(index, assignment) for h in self.head])


@dataclass(frozen=True)
class Iff:
    left: List[Atom]
    right: List[Atom]

    def atoms(self):
        for a in self.left:
            yield a
        for a in self.right:
            yield a

    def clausify(self, index):
        return [[-index.getLiteral(a)
                 for a in self.left] + [index.getLiteral(r)]
                for r in self.right
                ] + [[-index.getLiteral(a)
                      for a in self.right] + [index.getLiteral(l)]
                     for l in self.left]

    def collect(self, index):
        variables = set()
        for a in self.left:
            variables |= a.collect(index)
        for a in self.right:
            variables |= a.collect(index)
        return variables

    def show(self):
        left = ', '.join([a.show() for a in self.left])
        right = ', '.join([a.show() for a in self.right])
        return f"{left} <-> {right}"

    def evaluate(self, index, assignment):
        return Iff([l.evaluate(index, assignment) for l in self.left],
                   [r.evaluate(index, assignment) for r in self.right])


@dataclass(frozen=True)
class Or:
    disjuncts: List[Atom]

    def atoms(self):
        for a in self.disjuncts:
            yield a

    def clausify(self, index):
        return [[index.getLiteral(a) for a in self.disjuncts]]

    def collect(self, index):
        return reduce(union, [d.collect(index) for d in self.disjuncts], set())

    def show(self):
        return ' v '.join([a.show() for a in self.disjuncts])

    def evaluate(self, index, assignment):
        return Or([d.evaluate(index, assignment) for d in self.disjuncts])


@dataclass(frozen=True)
class Never:
    conjuncts: List[Atom]

    def atoms(self):
        for a in self.conjuncts:
            yield a

    def clausify(self, index):
        return [[-index.getLiteral(a) for a in self.conjuncts]]

    def collect(self, index):
        return reduce(union, [c.collect(index) for c in self.conjuncts], set())

    def show(self):
        conjuncts = ", ".join([a.show() for a in self.conjuncts])
        return f"{conjuncts} -> False"

    def evaluate(self, index, assignment):
        return Never([a.evaluate(index, assignment) for a in self.conjuncts])
