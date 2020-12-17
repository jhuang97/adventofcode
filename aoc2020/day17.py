import numpy as np

file1 = open('day_17_input.txt', 'r')
# file1 = open('day_17_test.txt', 'r')
dot_arr = [list(s) for s in file1.read().splitlines()]

n = [-1, 0, 1]
adjacent = [np.array([i, j, k]) for i in n for j in n for k in n if (i != 0 or j != 0 or k != 0)]
neighborhood = [np.array([i, j, k]) for i in n for j in n for k in n]

active = set()
for iy in range(len(dot_arr)):
    for ix in range(len(dot_arr[0])):
        if dot_arr[iy][ix] == '#':
            active.add((ix, iy, 0))

for k in range(6):
    to_check = set()
    for ctuple in active:
        for dr in neighborhood:
            to_check.add(tuple(np.asarray(ctuple) + dr))

    next_active = set()
    for ctuple in to_check:
        nactive = 0
        for dr in adjacent:
            if tuple(np.asarray(ctuple) + dr) in active:
                nactive += 1
        if ctuple in active:
            if nactive == 2 or nactive == 3:
                next_active.add(ctuple)
        else:
            if nactive == 3:
                next_active.add(ctuple)
    active = next_active

print(len(active))

# lolololol
n = [-1, 0, 1]
adjacent = [np.array([i, j, k, l]) for i in n for j in n for k in n for l in n if (i != 0 or j != 0 or k != 0 or l != 0)]
neighborhood = [np.array([i, j, k, l]) for i in n for j in n for k in n for l in n]

active = set()
for iy in range(len(dot_arr)):
    for ix in range(len(dot_arr[0])):
        if dot_arr[iy][ix] == '#':
            active.add((ix, iy, 0, 0))

for k in range(6):
    to_check = set()
    for ctuple in active:
        for dr in neighborhood:
            to_check.add(tuple(np.asarray(ctuple) + dr))

    next_active = set()
    for ctuple in to_check:
        nactive = 0
        for dr in adjacent:
            if tuple(np.asarray(ctuple) + dr) in active:
                nactive += 1
        if ctuple in active:
            if nactive == 2 or nactive == 3:
                next_active.add(ctuple)
        else:
            if nactive == 3:
                next_active.add(ctuple)
    active = next_active
print(len(active))