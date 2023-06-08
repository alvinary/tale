import pytest
from tale.objects import *

SEPARATOR = ";"

# Two trees, no root
model1 = [
    "left(a, b)", "left(d, e)", "right(a, c)", "right(d, f)", "left(f, g)",
    "right(f, h)"
]

# One short cycle
model2 = [
    s.strip() for s in
    "left(a, b) ; right(a, c) ; left(c, a) ; right(c, d)".split(SEPARATOR)
]

# Longer cycles
model3 = [
    s.strip() for s in
    "left(a, b) ; right(a, c) ; left(c, e) ; right(c, d) ; left(e, a) ; right(e, b)"
    .split(SEPARATOR)
]

# No left
model4 = [
    s.strip() for s in
    "left(a, b) ; right(a, c) ; right(c, d) ; left(b, e) ; right(b, f)".split(
        SEPARATOR)
]

# A tree
model5 = [
    s.strip() for s in
    "left(A, B) ; right(A, C) ; left(C, D); right(C, E)".split(SEPARATOR)
]


def test_trees():
    try:
        getTree(model1, test=True)
        assert False
    except BrokenPrecondition:
        pass

    try:
        getTree(model2, test=True)
        assert False
    except BrokenPrecondition:
        pass

    try:
        getTree(model3, test=True)
        assert False
    except BrokenPrecondition:
        pass

    try:
        getTree(model4, test=True)
        assert False
    except BrokenPrecondition:
        pass

    assert getTree(model5, test=True)

    assert getTree(model5, test=True).show() == "(B (D E))"
