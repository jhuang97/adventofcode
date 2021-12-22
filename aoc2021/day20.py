import numpy as np

fname = 'day_20_input.txt'
file1 = open(fname, 'r')
sections = file1.read().strip().split('\n\n')

rules = [1 if c == '#' else 0 for c in list(sections[0])]
# print(rules)
lines = sections[1].splitlines()
arr = []
for l in lines:
    arr.append([1 if c == '#' else 0 for c in l])
arr = np.array(arr, dtype=int)
# print(arr)

dark = int('000000000', 2)
light = int('111111111', 2)
# print(dark, light, rules[dark], rules[light])
rule_bkgd = [rules[dark], rules[light]]


def update(arr, bkgd, rules, rule_bkgd):
    nr, nc = np.shape(arr)
    arr = np.pad(arr, (2,), 'constant', constant_values=bkgd)
    new_arr = np.zeros((nr+2, nc+2), dtype=int)
    for r in range(nr+2):
        for c in range(nc+2):
            sub = arr[r:r+3, c:c+3]
            idx = int(''.join([str(n) for n in sub.flatten()]), 2)
            new_arr[r, c] = rules[idx]
    return new_arr, rule_bkgd[bkgd]


bkgd = 0
arr, bkgd = update(arr, bkgd, rules, rule_bkgd)
arr, bkgd = update(arr, bkgd, rules, rule_bkgd)
# print(bkgd)
print(np.sum(arr))

for _ in range(48):
    arr, bkgd = update(arr, bkgd, rules, rule_bkgd)
print(np.sum(arr))