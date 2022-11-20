import graphviz
import json
import sys

dot = graphviz.Digraph('pipelines-diagram', comment='Project Diagram')
dot.attr('graph', splines='ortho')
dot.attr('node', fontname='Arial')

config = json.load(open(sys.argv[1],'r'))
for i in config['result']:
    dot.node(i['id'],i['pipeline'], shape='box')
    if 'connection' in i.keys():
        dot.edge(i['connection'],i['id'])

#dot.render(outfile=f'/opt/snaplogic/diagrams/{sys.argv[2]}.png')
