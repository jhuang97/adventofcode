import numpy as np
from collections import defaultdict

file1 = open('day_12_input.txt', 'r')
lines = file1.read().strip().split('\n')
# lines = """dc-end
# HN-start
# start-kj
# dc-start
# dc-HN
# LN-dc
# HN-end
# kj-sa
# kj-HN
# kj-dc""".splitlines()

neighbors = defaultdict(list)
for l in lines:
    parts = l.split('-')
    neighbors[parts[0]].append(parts[1])
    neighbors[parts[1]].append(parts[0])


def num_ways(path):
    node = path[-1]
    total = 0
    for n in neighbors[node]:
        if n == 'end':
            total += 1
        elif n.isupper() or (n.islower() and n not in path):
            total += num_ways(path + (n,))
    return total


print(num_ways(('start',)))


def num_ways_2(path, small_twice):
    node = path[-1]
    total = 0
    for n in neighbors[node]:
        if n == 'end':
            total += 1
        elif n.isupper():
            total += num_ways_2(path + (n,), small_twice)
        elif n.islower() and n != 'start':
            if n in path:
                if not small_twice:
                    total += num_ways_2(path + (n,), True)
            else:
                total += num_ways_2(path + (n,), small_twice)
    return total


print(num_ways_2(('start',), False))