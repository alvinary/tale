import sys

trash = '''
The input program is satfiable .

Showing one model ...

Model 1:'''

def to_gv (text):
    edges = text.split("\n")
    edges = [' -> '.join(s.replace("left(", "").replace(")", "").replace("right(", "").split(",")) for s in edges if s.strip()]
    edges = ";\n  ".join(edges)
    return "Digraph {\n" + edges + "\n}"

graph_data = ''
for line in sys.stdin:
    graph_data += line

for trash_item in trash.split():
    graph_data = graph_data.replace(trash_item, "")

while "\n\n" in graph_data:
    graph_data = graph_data.replace("\n\n", "\n")

print(to_gv(graph_data))
