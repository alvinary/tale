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

    functions = application | several
    application = "." fun:name
    several = "." fun:name rest:application 

    rule
        =
        | if
        | iff
        | never
        | or

    if = body:atoms '->' head:atoms
    iff = left:atoms '<->' right:atoms
    never = conjuncts:atoms '->' 'False'
    or = atomd

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
              | manya
              | lasta

    manya = head:term "," tail:arguments
    lasta = end:term

    plain = term

    comparison = left:term op:operator right:term

    operator = nequals | equals | get | gt

    nequals = '!='
    equals = '='
    get = '<='
    ge = '<'
'''

class ProgramSemantics:
    def name(self, ast):
        return str(ast)
    def program(self, ast):
        return ast
    def programpart(self, ast):
        return ast.current + ast.next
    def finalstatement(self, ast):
        return [ast.last]
    def statement(self, ast):
        return [ast]
    def comment(self, ast):
        return []
    def term(self, ast):
        return Term(ast.main, ast.funs)
    def functions(self, ast):
        return ast
    def application(self, ast):
        return [ast.name]
    def several(self, ast):
        return [ast.fun] + ast.rest
    def rule(self, ast):
        return ast
    def if(self, ast):
        return If(ast.body, ast.head)
    def iff(self, ast):
        return Iff(ast.left, ast.right)
    def never(self, ast):
        return Never(ast.conjuncts)
    def or(self, ast):
        return Or(ast)
    def atomd(self, ast):
        return ast
    def manyd(self, ast):
        return [ast.head] + ast.tail
    def lastd(self, ast):
        return [ast.end]
    def atom(self, ast):
        return ast
    def predicate(self, ast):
        return Atom([ast.term] + ast.args)
    def arguments(self, ast):
        return ast
    def manya(self, ast):
        return [ast.head] + ast.tail
    def lasta(self, ast):
        return [ast.end]
    def plain(self, ast):
        return ast
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

