from tale.programs import *

testProgram = '''
-- This is a comment.
-- This is a comment too.
fill c 4 : const, comp.
var a, b : const.
var F : fun.
f, g, h : fun.
let g : const -> const.
let f : const -> const.
let h : const -> const.
let y : const, const -> const.

-- Mind you, there
-- are no block comments.

let a.h = b.
let a.g = a.
let b.h = b.
let b.h = a.

a.F.g = a.F.g, g = f.F <-> fun(F).
p (a, b.h), q (b) -> r (a, b), s(b, a).
n (a) v m (a).
either p (a), not p (a).
'''


def test_parser():
    _, _, _, _, content = parseProgram(testProgram)
    assert len(content) == 4
    for rule in content:
        print(rule)
        print(type(rule))
        print('')
        checks = False
        checks = checks or isinstance(rule, Or)
        checks = checks or isinstance(rule, Either)
        checks = checks or isinstance(rule, If)
        checks = checks or isinstance(rule, Never)
        checks = checks or isinstance(rule, Iff)
        assert checks


def test_declarations():
    sorts, variables, values, functions, _ = parseProgram(testProgram)
    a = Term('a', [])
    b = Term('b', [])
    c1 = Term('c1', [])
    c3 = Term('c3', [])
    f = Term('f', [])
    F = Term('F', [])
    y = Term('y', [])

    assert c1 in sorts['const']
    assert c3 in sorts['const']
    assert c1 in sorts['comp']
    assert c3 in sorts['comp']
    assert f in sorts['fun']
    assert 'F' in variables.keys()
    assert 'a' in variables.keys()
    assert 'f' in values.keys()
    assert 'g' in values.keys()
    assert variables['F'] == 'fun'
    assert variables['a'] == 'const'
    assert values['f'] == (['const'], 'const')
    assert values['y'] == (['const', 'const'], 'const')
    assert functions['h', 'a'] == 'b'
    assert functions['h', 'b'] == 'a'


def test_negation():
    pass
