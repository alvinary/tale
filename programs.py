import tatsu
from tatsu.ast import AST

from tale.formulas import *

grammar = ''' 
    @@grammar::Program

    start = preamble:declarations rules:program $ ;

    declarations = declarationspart | finaldeclaration ;

    declarationspart = current:declaration next:declarations ;

    declaration = cont:declare "." ;

    declare
        =
        | add
        | fill
        | let
        | var
        ;

    add = elems:elements  ":" sort:name ;
    fill = "fill " prefix:name n:number ":" sort:name ;
    var = "var " vars:elements ":" sort:name ;
    let = "let " f:name ":" domain:name "->" range:name ;

    number = n:/[0-9]+/ ;

    elements = lastelem | manyelems ;
    lastelem = last:element ;
    manyelems = current:element rest:elements ;

    finaldeclaration = last:declaration ;

    name = /[A-Za-z0-9]+/ ;

    program = programpart | finalstatement ;

    programpart = current:statement next:program ;
    finalstatement = last:statement ;

    term = functional | simple ;
    functional = main:name funs:functions ;
    simple = main:name ;

    functions = several | application ;
    application = "." fun:name ;
    several = "." fun:name rest:functions ;

    rule
        =
        | horn
        | iff
        | never
        | disjunction
        | either ;

    horn = body:atoms '->' head:atoms ;
    iff = left:atoms '<->' right:atoms ;
    never = conjuncts:atoms '->' 'False' ;
    disjunction = atomd ;
    either = 'either ' options:atoms ;

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
        | lastatom ;

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

class ProgramSemantics:
    def name(self, ast):
        return str(ast)
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
        return ast
    def application(self, ast):
        return [ast.name]
    def several(self, ast):
        return [ast.fun] + list(ast.rest)
    def rule(self, ast):
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
    def atom(self, ast):
        return ast
    def negative(self, ast):
        return ast.pred.negate()
    def predicate(self, ast):
        return Atom([ast.term] + list(ast.args))
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

