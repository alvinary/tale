from cyk import *
from collections import defaultdict

TYPE = 'type'
VALUE = 'value'

inventory = lambda: defaultdict(lambda: [])


class State:

    def __init__(self):
        self.defined = set()
        self.types = {}
        self.values = {}
        self.args = inventory()

    def crash(self):
        exit()


state = State()


def nameError(name):
    print(f"`{name}` is not defined!")
    state.crash()


def typeError(identifier, intendedType, expression):
    print(f"")


def returnError():
    print(f"")


def voidError(functionName):
    print("Functions must have a return value!")
    print("However, function {functionName} does not have a return value.")


def mismatchError(function, t, s):
    print(
        "{function} was declared as {t}, but its return variable is of type {s}."
    )


def conditional(condition, statement, otherwise=False):
    if condition:
        statement()
    if otherwise:
        otherwise()


def definition(name, args, t, statement):
    state.types[name] = t
    state.values[name] = statement
    state.args[name] = args


def call(function, arguments):
    # check types
    pass


def defineType(name, expression):
    pass


def assignment(name, expression):
    if name not in state.defined:
        nameError(name)
    if state.types[name] == expression[TYPE]:
        state.values[name] = expression[VALUE]
    else:
        typeError(name, state.types[name], expression)
