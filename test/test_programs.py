from tale.programs import *

testProgram = '''
fill c 4 : const.
var a, b : const.
var F : fun.
f, g, h : fun.
let g : const -> const.
let f : const -> const.
let h : const -> const.

a.F.g = a.F.g, g = f.F <-> fun(F).
p (a, b.h), q (b) -> r (a, b), s(b, a).
n (a) v m (a).
either p (a), not p (a).
'''

def test_parser():
    _, _, _, content = parseProgram(testProgram)
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
        
def test_negation():
    pass

