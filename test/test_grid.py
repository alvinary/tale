from inspect import getsourcefile
from os.path import abspath

from tale.objects import getTree
from tale.pipeline import pipeline
from tale.formulas import Term

MODELS = 3

path_prefix = str(abspath(getsourcefile(lambda:0)))
model_path = path_prefix.replace('tale/test/test_grid.py', 'tale/models/grid_trees.tl')

program = ''
with open(model_path, 'r') as grid_trees:
    for line in grid_trees:
        program += line

def test_grid():
    print('Assembling grid...')
    sorts = {'tree' : []}
    values = {}
    for i in range(6):
        for j in range(6):
            const = f't_{i}_{j}'
            left = f't_{i+1}_{j}'
            right = f't_{i}_{j+1}'
            sorts['tree'].append(Term(const, []))
            values['left', const] = left
            values['right', const] = right

    print('Computing models...')
    models = pipeline(program, default_functions=values, default_sorts=sorts)


    if not models:
        assert False
    print('Showing models...')
    if models:
        for index, model in zip(range(MODELS), models):
            tree = getTree(model)
            if tree:
                print(tree.show())
            else:
                print("\n".join(model))

if __name__ == '__main__':
    test_grid()
