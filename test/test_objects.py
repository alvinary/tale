import pytest
from tale.objects import *

SEPARATOR = ";"

# Two trees, no root
model1 = ["left(a, b)", "left(d, e)", "right(a, c)", "right(d, f)", "left(f, g)", "right(f, h)"]

# One short cycle
model2 = "left(a, b) ; right(a, c) ; left(c, a) ; right (c, d)".split(SEPARATOR)

# Longer cycles
model3 = "left(a, b) ; right(a, c) ; left(c, e) ; right (c, d) ; left (e, a) ; right (e, b)".split(SEPARATOR)

# No left
model4 = "left(a, b) ; right (a, c) ; right (c, d) ; left (b, e) ; right (b, f)".split(SEPARATOR)

# A tree
model5 = "left (1, 2) ; right (1, 3) ; left (3, 4); right (3, 5)".split(SEPARATOR)

def test_trees():
    try:
        getTree(model1)
        assert False
    except BrokenPrecondition:
        pass

    try:
        getTree(model2)
        assert False
    except BrokenPrecondition:
        pass

    try:
        getTree(model3)
        assert False
    except BrokenPrecondition:
        pass

    try:
        getTree(model4)
        assert False
    except BrokenPrecondition:
        pass

    assert getTree(model5)
