from collections import defaultdict
from dataclasses import dataclass
from itertools import product
from typing import List
from functools import reduce

union = lambda x, y: x | y


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
        return f"No value found for {term}.{function}."

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

    def addRule(self, rule):

        if isinstance(rule, Comparison):
            self.addAtom(rule)
        if isinstance(rule, Iff):
            for a in rule.left:
                self.addAtom(a)
            for a in rule.right:
                self.addAtom(a)
        if isinstance(rule, Or):
            for a in rule.disjuncts:
                self.addAtom(a)
        if isinstance(rule, Never):
            for a in rule.conjuncts:
                self.addAtom(a)
        if isinstance(rule, Either):
            for a in rule.options:
                self.addAtom(a)
        if isinstance(rule, If):
            for a in rule.head:
                self.addAtom(a)
            for a in rule.body:
                self.addAtom(a)


class Index:

    def __init__(self, values={}, sorts={}, variables={}):

        self.valueMap = values
        self.sortMap = sorts
        self.variableMap = variables

    def toDimacs(self, atom):
        return self.dimacsMap[atom]

    def fromDimacs(self, atom):
        return self.stringMap[atom]

    def value(self, function, elem):

        if (function, elem) in self.valueMap.keys():
            value = self.valueMap[function, elem]
            error = Ok()
        else:
            value = None
            error = FunctionError(function, elem)

        return value, error

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

        for elem in self.sortMap[sort]:
            yield elem

    def assignments(self, variables):
        sorts = [self.variableMap[v] for v in variables]
        for assignment in product(*[self.sortMap[s] for s in sorts]):
            binding = dict(zip(variables, assignment))
            yield Assignment(binding)


@dataclass(frozen=True)
class Term:
    term: str
    functions: list[str]

    def evaluate(self, index, assignment):

        _functions = list(self.functions)
        argument = self.term

        while _functions:
            function = _functions.pop(0)
            if index.hasVariable(function):
                function, error = assignment.bind(function)
            value, error = index.value(function, argument)
            argument = value

        if not self.functions and index.hasVariable(argument):
            value, error = assignment.bind(argument)

        if not self.functions and not index.hasVariable(argument):
            value, error = argument, Ok()

        return value, error

    def collect(self, index):

        names = [self.term] + self.functions
        return {n for n in names if index.hasVariable(n)}

    def show(self):
        return f"{self.term}{''.join(['.' + f for f in self.functions])}"


@dataclass(frozen=True)
class Atom:
    terms: List[Term]

    def evaluate(self, index, assignment):
        return Atom([t.evaluate(index, assignment)] for t in self.terms)

    def collect(self, index):
        variables = set()
        for t in self.terms:
            variables |= t.collect(index)
        return variables

    def show(self):
        predicate = self.terms[0].show()
        arguments = [a.show() for a in self.terms[1:]]
        return f"{predicate}({', '.join(arguments)})"


@dataclass(frozen=True)
class Comparison:
    comparison: str
    left: Term
    right: Term

    def clausify(self, index):
        return [[index.getLiteral(self)]]

    def collect(self, index):
        variables = set()
        for t in self.left:
            variables |= t.collect(index)
        for t in self.right:
            variables |= t.collect(index)
        return variables

    def show(self):
        return f"{self.left.show()} {self.comparison} {self.right.show()}"


@dataclass(frozen=True)
class Either:
    options: List[Atom]

    def clausify(self, index):
        return [[index.getLiteral(o) for o in self.options]] + [[
            -index.getLiteral(o1), -index.getLiteral(o2)
        ] for o1, o2 in product(self.options, self.options) if o1 != o2]

    def collect(self, index):
        return reduce(union, [o.collect(index) for o in self.options], set())

    def show(self):
        return f"Either {', '.join([a.show() for a in self.options])}"


@dataclass(frozen=True)
class If:
    body: List[Atom]
    head: List[Atom]

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
        return f"{body} => {head}"


@dataclass(frozen=True)
class Iff:
    left: List[Atom]
    right: List[Atom]

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
            variables |= a.collect()
        for a in self.right:
            variables |= a.collect()
        return variables

    def show(self):
        left = ', '.join([a.show() for a in self.left])
        right = ', '.join([a.show() for a in self.right])
        return f"{left} <=> {right}"


@dataclass(frozen=True)
class Or:
    disjuncts: List[Atom]

    def clausify(self, index):
        return [[index.getLiteral(a) for a in self.disjuncts]]

    def collect(self, index):
        return reduce(union, [d.collect(index) for d in self.disjuncts], set())

    def show(self):
        return ' v '.join([a.show() for a in self.disjuncts])


@dataclass(frozen=True)
class Never:
    conjuncts: List[Atom]

    def clausify(self, index):
        return [[-index.getLiteral(a) for a in self.conjuncts]]

    def collect(self, index):
        return reduce(union, [c.collect(index) for c in self.conjuncts], set())

    def show(self):
        conjuncts = ", ".join([a.show() for a in self.conjuncts])
        return f"{conjuncts} => False"
