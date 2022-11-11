from tale.programs import *

testProgram = '''
a.F.g = a.F.g, g = f.F <-> fun(F).
p (a, b.h), q (b) -> r (a, b), s(b, a).
n (a) v m (a).
either p (a), not p (a).
'''

def test_parser():
    content = list(parseProgram(testProgram))
    print(len(content))
    assert isinstance(content, list)
    for rule in content:
        print(rule)
        print('')
        checks = False
        checks = checks or isinstance(rule, Or)
        checks = checks or isinstance(rule, Either)
        checks = checks or isinstance(rule, If)
        checks = checks or isinstance(rule, Never)
        checks = checks or isinstance(rule, Iff)
    assert False
