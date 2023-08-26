from inspect import getsourcefile
from os.path import abspath

from tale.objects import getTree
from tale.pipeline import Program
from tale.formulas import Term

MODELS = 6

path_prefix = str(abspath(getsourcefile(lambda:0)))
model_path = path_prefix.replace('tale/test/test_grid.py', 'tale/models/grid_trees.tl')

program = ''
with open(model_path, 'r') as grid_trees:
    for line in grid_trees:
        program += line

def relevant(fact):
    return 'not' not in fact and '=' not in fact and (
        'right' in fact or
        'left' in fact or
        'class' in fact or
        'vr' in fact or
        'vl' in fact)

def test_grid():
    print('Assembling grid...')
    sorts = {'tree' : [], 'nonroot' : []}
    functions = {}
    for i in range(5):
        for j in range(5):
            const = f't_{i}_{j}'
            left = f't_{i+1}_{j}'
            right = f't_{i}_{j+1}'
            term = Term(const, [])
            sorts['tree'].append(term)
            functions['left', const] = left
            functions['right', const] = right
            if i != 0 or j != 0:
                sorts['nonroot'].append(term)

    print('Computing models...')
    models = Program(program, defaultFunctions=functions, defaultSorts=sorts).models()

    if not models:
        assert False
    print('Showing models...')
    if models:
        for index, model in zip(range(MODELS), models):
            model = [f for f in model if relevant(f)]
            print("\n".join(list(sorted(model))))
            print("\n"*5)

if __name__ == '__main__':
    test_grid()
