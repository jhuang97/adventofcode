import numpy as np
from collections import defaultdict

file1 = open('day07_in.txt', 'r')
# file1 = open('day07_test.txt', 'r')

lines = file1.read().strip().split('\n')

child_file = defaultdict(list)
child_dir = defaultdict(list)
filesize = {}


def child(parent, cname):
    if parent == '/':
        return '/' + cname
    return parent + '/' + cname


def get_dir(curr_dir, arg):
    if arg == '/':
        return '/'
    elif arg == '..':
        out = curr_dir[:curr_dir.rindex('/')]
        if len(out) == 0:
            return '/'
        else:
            return out
    else:
        return child(curr_dir, arg)


def update(curr_dir, lslines):
    for l in lslines:
        if l.startswith('dir '):
            child_dir[curr_dir].append(child(curr_dir, l[4:]))
        else:
            parts = l.split()
            sz = int(parts[0])
            fname = child(curr_dir, parts[1])
            child_file[curr_dir].append(fname)
            filesize[fname] = sz


curr_dir = ''
lidx = 0
while lidx < len(lines):
    curr_l = lines[lidx]
    if curr_l.startswith('$ cd '):
        # print('cd from', curr_dir)
        curr_dir = get_dir(curr_dir, curr_l[5:])
        # print('cd to', curr_dir, curr_l[5:])
        lidx += 1
    elif curr_l.startswith('$ ls'):
        end_idx = lidx + 1
        while end_idx < len(lines) and lines[end_idx][0] != '$':
            end_idx += 1
        update(curr_dir, lines[lidx+1:end_idx])
        lidx = end_idx
    else:
        print('oh no')


dir_sizes = {}


def get_dir_size(root):
    if root in dir_sizes:
        return dir_sizes[root]
    total = 0
    for child_d in child_dir[root]:
        total += get_dir_size(child_d)
    for child_f in child_file[root]:
        total += filesize[child_f]
    dir_sizes[root] = total
    return total


get_dir_size('/')
# print(dir_sizes)

total = 0
for d, dsize in dir_sizes.items():
    if dsize <= 100000:
        total += dsize
print(total)


total_space = 70000000
needed_unused = 30000000
current_unused = total_space - get_dir_size('/')
need_to_free_up = needed_unused - current_unused
d_arr = np.array(list(dir_sizes.values()))
best_size = np.min(d_arr[d_arr >= need_to_free_up])
print(best_size)


import networkx as nx
import matplotlib.pyplot as plt
import pydot
from networkx.drawing.nx_pydot import graphviz_layout

DG = nx.DiGraph()

def make_graph(root):
    for child_d in child_dir[root]:
        DG.add_edge(root, child_d)
        make_graph(child_d)
    for child_f in child_file[root]:
        DG.add_edge(root, child_f)


make_graph('/')
pos = graphviz_layout(DG, prog="dot")
nx.draw(DG, pos, node_size = 10)
plt.show()