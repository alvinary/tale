import tatsu
from tatsu.ast import AST

programs = ''' 
    @@grammar::Program

    start = program $ ;

    program = programpart | finalstatement

    programpart = current:statement next:program
    finalstatement = last:statement

    statement
        = 
        | comment "."
        | rule "."
        ;

    comment = '*' ?/[^\.]+/

    term = main:name funs:functions

    functions = ("." name)*

    rule
        =
        | if
        | iff
        | never
        | or

    if = body:atoms '->' head:atoms
    iff = left:atoms '<->' right:atoms
    never = conjuncts:atoms '->' 'False'
    or = atomdisjunction

    atom
        =
        | predicate
        | comparison
        | plain

    predicate = predicate:term "(" args:arguments ")"

    atoms
        =
        | manyatoms
        | lastatom

    manyatoms = head:atom "," tail:atoms
    lastatom = end:atom

    atomd = manyd | lastd
    manyd = head:atom "v" tail:atomd
    lastd = end:atom

    arguments =
              | many
              | last

    many = head:term "," tail:arguments
    last = end:term

    plain = term

    comparison = left:term op:operator right:term

    operator = nequals | equals | get | gt

    nequals = '!='
    equals = '='
    get = '<='
    ge = '<'

'''

class Interpretation:
    def operator(self, ast):
        return ast
    def comparison(self, ast):
        return ast
    def statement(self, ast):
        return ast
    def term(self, ast):
        return ast

