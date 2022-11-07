from collections import defaultdict
from dataclasses import dataclass
from typing import List

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
        self.assignment = mapping
        
    def bind(self, term):
        if term in self.assignment.keys():
            return self.assignment[term], Ok()
        else:
            return None, AssignmentError(term)

class DimacsIndex:

    def __init__(self, atoms):        
        self.dimacsMap = {}
        self.stringMap = {}
        self.counter = 0

        for atom in atoms:
            self.addAtom(atom)
            
    def toDimacs(self, atom):
        return self.dimacsMap[atom]
        
    def fromDimacs(self, dimacs):
        return self.stringMap[dimacs]
        
    def addAtom(self, atom):
        while self.counter in self.stringMap.keys():
            self.counter += 1
        dimacs_atom = self.counter
        self.dimacsMap[atom] = dimacs_atom
        self.stringMap[dimacs_atom] = atom
        self.counter += 1
        
    def getLiteral(self, atom):
        if atom in self.dimacsMap.keys():
            return self.toDimacs(atom)
        else:
            self.addAtom(atom)
            return self.toDimacs(atom)

class Index:

    def __init__(self, values={},
                       sorts={},
                       variables={}):

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

    def isVariable(self, name):
        return name in self.variableMap.keys()
        
    def assignments(self, sorts):
        pass
        #for t in product():
        #    yield assignment

@dataclass(frozen=True)
class Term:
    term : str
    functions : list[str]

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
            value, error = assignment.bind(c24b296f38562a16f811bc1b35b1f3f73860e65fargument)

        if not self.functions and not index.hasVariable(argument):
            value, error = argument, Ok()

        return value, error
        
    def show(self):
        return f"{self.term}.{'.'.join(self.functions)}"

@dataclass(frozen=True)
class Atom:
    terms : List[Term]
    
    def evaluate(self, index, assignment):
        return Atom([t.evaluate(index, assignment)] for t in self.terms)
        
    def show(self):
        return f"{self.terms[0]}({','.join(self.terms[1:])})"
        
@dataclass(frozen=True)
class Comparison:
    left : Term
    right : Term

@dataclass(frozen=True)
class Either:
    options : List[Atom]

@dataclass(frozen=True)
class If:
    body : List[Atom]
    head : List[Atom]

@dataclass(frozen=True)
class Iff:
    left : List[Atom]
    right : List[Atom]

@dataclass(frozen=True)
class Or:
    disjuncts : List[Atom]
    
    def clausify(self, index):
        return [-index.getLiteral(a) for a in self.disjuncts]

@dataclass(frozen=True)
class Never:
    conjuncts : List[Atom]

