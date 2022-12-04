file1 = open('day04_in.txt', 'r')
lines = file1.read().strip().split('\n')
pairs = [[[int(n) for n in r.split('-')] for r in l.split(',')] for l in lines]


def fcontain(pair):
    l1, h1, l2, h2 = pair[0][0], pair[0][1], pair[1][0], pair[1][1]
    return (l1 <= l2 and h2 <= h1) or (l2 <= l1 and h1 <= h2)


def overlap(pair):
    l1, h1, l2, h2 = pair[0][0], pair[0][1], pair[1][0], pair[1][1]
    return not (h1 < l2 or h2 < l1)


total = 0
total2 = 0
for p in pairs:
    if fcontain(p):
        total += 1
    if overlap(p):
        total2 += 1
print(total)
print(total2)