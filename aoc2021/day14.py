import numpy as np
from itertools import chain, zip_longest
from collections import defaultdict

file1 = open('day_14_input.txt', 'r')
lines = file1.read().strip().split('\n\n')
# lines = """NNCB
#
# CH -> B
# HH -> N
# CB -> H
# NH -> C
# HB -> C
# HC -> B
# HN -> C
# NN -> C
# BH -> H
# NC -> B
# NB -> B
# BN -> B
# BB -> N
# BC -> B
# CC -> N
# CN -> C
# """.split('\n\n')

poly = list(lines[0])
r_lines = lines[1].splitlines()
rules = {}
for l in r_lines:
    sides = l.split(' -> ')
    rules[(sides[0][0], sides[0][1])] = sides[1]


def twolists(l1, l2):
    return [x for x in chain.from_iterable(zip_longest(l1, l2)) if x is not None]


for _ in range(10):
    middle_elems = []
    for k in range(len(poly)-1):
        middle_elems.append(rules[(poly[k], poly[k+1])])
    poly = twolists(poly, middle_elems)


freqs = defaultdict(int)
for c in poly:
    freqs[c] += 1
# print(freqs)

freq_int = np.array(list(freqs.values()))
print(np.max(freq_int) - np.min(freq_int))


poly = list(lines[0])
pair_freqs = defaultdict(int)
for k in range(len(poly)-1):
    pair_freqs[(poly[k], poly[k+1])] += 1

rules2 = {}
for l in r_lines:
    sides = l.split(' -> ')
    rules2[(sides[0][0], sides[0][1])] = ((sides[0][0], sides[1]), (sides[1], sides[0][1]))

for _ in range(40):
    new_pair_freqs = defaultdict(int)
    for pair, freq in pair_freqs.items():
        pair1, pair2 = rules2[pair]
        new_pair_freqs[pair1] += freq
        new_pair_freqs[pair2] += freq
    pair_freqs = new_pair_freqs.copy()
final_freqs = defaultdict(int)
for pair, freq in pair_freqs.items():
    final_freqs[pair[0]] += freq
    final_freqs[pair[1]] += freq
final_freqs[poly[0]] += 1
final_freqs[poly[-1]] += 1
# print(final_freqs)
freq_int = np.array(list(final_freqs.values()))/2
print(int(np.max(freq_int) - np.min(freq_int)))