from tale.programs import *

testProgram = '''
* This is a test program.
* This should test comments work properly.

a.F.g = a.F.g, g = f.F <-> fun(F).
p (a, b.h), q (b) -> r (a, b), s(b, a).
n (a) v m (a).
either p (a), not p (a).

* Did this work? Let's try it out.
'''

def test_parser():
    content = parseProgram(testProgram)
    assert isinstance(content, list)
    for rule in content:
        print(rule.show())
        checks = False
        checks = checks or isinstance(rule, Or)
        checks = checks or isinstance(rule, Either)
        checks = checks or isinstance(rule, If)
        checks = checks or isinstance(rule, Never)
        checks = checks or isinstance(rule, Iff)
        assert checks
