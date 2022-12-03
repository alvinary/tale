from collections import defaultdict

import tatsu
from tatsu.ast import AST

from tale.formulas import *
from tale.embeddings import *

listMap = lambda: defaultdict(lambda: [])

grammar = ''' 
    @@grammar::Program

    start = fullprogram $ ;
    
    fullprogram = preamble:declarations rules:program ;

    declarations = declarationspart | finaldeclaration ;

    declarationspart = current:declaration next:declarations ;

    declaration = cont:declare "." ;

    declare
        =
        | add
        | fill
        | let
        | var
        | order
        | assign
        ;

    add = elems:elements ":" sort:name ;
    fill = "fill " prefix:name n:number ":" sort:name ;
    var = "var " vars:elements ":" sort:name ;
    let = "let " f:name ":" domain:elements "->" range:name ;
    order = "order " prefix:name n:number ":" sort:name ;
    assign = "let " preimage:name "." f:name "=" image:name ;

    number = n:/[0-9]+/ ;

    elements = manyelems | lastelem ;
    manyelems = current:name "," rest:elements ;
    lastelem = last:name ;

    finaldeclaration = last:declaration ;

    name = /[A-Za-z0-9]+/ ;

    program = programpart | finalstatement ;

    programpart = current:statement next:program ;
    finalstatement = last:statement ;

    term = functional | simple ;
    functional = main:name "." funs:functions ;
    simple = main:name ;

    functions = several | application ;
    application = fun:name ;
    several = fun:name "." rest:functions ;

    rule
        =
        | never
        | horn
        | iff
        | disjunction
        | either 
        | assertion
        ;

    horn = body:atoms '->' head:atoms ;
    iff = left:atoms '<->' right:atoms ;
    never = conjuncts:atoms '->' 'False' ;
    disjunction = atomd ;
    either = 'either ' options:atoms ;
    assertion = asserted:atom ;

    atom
        =
        | predicate
        | comparison
        | negative;

    negative = 'not ' pred:predicate ;

    predicate = predicate:term "(" args:arguments ")" ;

    atoms
        =
        | manyatoms
        | lastatom
        ;

    manyatoms = head:atom "," tail:atoms ;
    lastatom = end:atom ;

    atomd = manyd | lastd ;
    manyd = head:atom "v" tail:atomd ;
    lastd = end:atom ;

    arguments =
              | manya 
              | lasta ;

    manya = head:term "," tail:arguments ;
    lasta = end:term ;

    comparison = left:term op:operator right:term ;

    operator = nequals | equals | get | ge ;

    nequals = '!=' ;
    equals = '=' ;
    get = '<=' ;
    ge = '<' ;

    statement = cont:rule "." ;
'''


def merge(left, right):
    leftSorts, leftVariables, leftValues, leftFunctions = left
    rightSorts, rightVariables, rightValues, rightFunctions = right
    for key in rightSorts.keys():
        for elem in rightSorts[key]:
            leftSorts[key].append(elem)
    leftVariables = leftVariables | rightVariables
    leftValues = leftValues | rightValues
    leftFunctions = leftFunctions | rightFunctions
    return leftSorts, leftVariables, leftValues, leftFunctions


class ProgramSemantics:

    def name(self, ast):
        return str(ast)

    def number(self, ast):
        return int(ast.n)

    def elements(self, ast):
        return list(ast)

    def lastelem(self, ast):
        return [ast.last]

    def manyelems(self, ast):
        return [ast.current] + list(ast.rest)

    def declarations(self, ast):
        return ast

    def declaration(self, ast):
        return ast.cont

    def finaldeclaration(self, ast):
        return ast.last

    def declarationspart(self, ast):
        return merge(ast.current, ast.next)

    def declare(self, ast):
        return ast

    def add(self, ast):
        sorts, variables, values, functions = listMap(), {}, {}, {}
        for elem in ast.elems:
            elem = Term(elem, [])
            sorts[ast.sort].append(elem)
        return sorts, variables, values, functions

    def fill(self, ast):
        sorts, variables, values, functions = listMap(), {}, {}, {}
        indexTerms = [Term(f"{ast.prefix}{i}", []) for i in range(ast.n)]
        sorts[ast.sort] += indexTerms
        return sorts, variables, values, functions

    def order(self, ast):
        left = listMap(), {}, {}, {}
        right = totalOrder(ast.n, ast.prefix, ast.sort)
        return merge(left, right)

    def assign(self, ast):
        return listMap(), {}, {}, {(ast.f, ast.preimage): ast.image}

    def var(self, ast):
        sorts, variables, values, functions = listMap(), {}, {}, {}
        for var in ast.vars:
            variables[var] = ast.sort
        return sorts, variables, values, functions

    def let(self, ast):
        sorts, variables, values, functions = listMap(), {}, {}, {}
        values[ast.f] = (ast.domain, ast.range)
        return sorts, variables, values, functions

    def fullprogram(self, ast):
        sorts, variables, values, functions = ast.preamble
        return sorts, variables, values, functions, ast.rules

    def program(self, ast):
        return ast

    def programpart(self, ast):
        return list(ast.current) + list(ast.next)

    def finalstatement(self, ast):
        return ast.last

    def statement(self, ast):
        return [ast.cont]

    def comment(self, ast):
        return []

    def term(self, ast):
        return ast

    def functional(self, ast):
        return Term(ast.main, ast.funs)

    def simple(self, ast):
        return Term(ast.main, [])

    def functions(self, ast):
        return list(ast)

    def application(self, ast):
        return [ast.fun]

    def several(self, ast):
        return [ast.fun] + list(ast.rest)

    def rule(self, ast):
        return ast

    def assertion(self, ast):
        return ast

    def horn(self, ast):
        return If(ast.body, ast.head)

    def iff(self, ast):
        return Iff(ast.left, ast.right)

    def never(self, ast):
        return Never(ast.conjuncts)

    def disjunction(self, ast):
        return Or(ast)

    def either(self, ast):
        return Either(ast.options)

    def atomd(self, ast):
        return ast

    def manyd(self, ast):
        return [ast.head] + list(ast.tail)

    def lastd(self, ast):
        return [ast.end]

    def manyatoms(self, ast):
        return [ast.head] + list(ast.tail)

    def lastatom(self, ast):
        return [ast.end]

    def atom(self, ast):
        return ast

    def atoms(self, ast):
        return ast

    def negative(self, ast):
        return ast.pred.negate()

    def predicate(self, ast):
        return Atom([ast.predicate] + list(ast.args))

    def arguments(self, ast):
        return ast

    def manya(self, ast):
        return [ast.head] + list(ast.tail)

    def lasta(self, ast):
        return [ast.end]

    def operator(self, ast):
        return str(ast)

    def comparison(self, ast):
        return Comparison(ast.op, ast.left, ast.right)

    def nequals(self, ast):
        return '!='

    def equals(self, ast):
        return '='

    def get(self, ast):
        return '<='

    def ge(self, ast):
        return "<"


def parseProgram(text):
    parser = tatsu.compile(grammar)
    interpretation = ProgramSemantics()
    return parser.parse(text, semantics=interpretation)
