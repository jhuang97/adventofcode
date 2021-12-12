import numpy as np

file1 = open('day_11_input.txt', 'r')
lines = file1.read().strip().split('\n')

# lines = """5483143223
# 2745854711
# 5264556173
# 6141336146
# 6357385478
# 4167524645
# 2176841721
# 6882881134
# 4846848554
# 5283751526""".split('\n')


octopuses = np.array([[int(c) for c in l] for l in lines], dtype=int)
dirs = [(-1, 0), (1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]


def neighbors(pt, arr):
    out = []
    r, c = pt
    for dr, dc in dirs:
        r2 = r+dr
        c2 = c+dc
        if 0 <= r2 < len(arr) and 0 <= c2 < len(arr[0]):
            out.append((r2, c2))
    return out


def at(pt, arr):
    return arr[pt[0], pt[1]]


def step(arr):
    flashed = np.zeros(np.shape(arr), dtype=int)
    arr += 1
    # print(fx, fy)
    changed = True
    while changed:
        changed = False
        fx, fy = np.nonzero(arr > 9)
        for k in range(len(fx)):
            pt = (fx[k], fy[k])
            if at(pt, flashed) == 0:
                for r2, c2 in neighbors(pt, arr):
                    arr[r2, c2] += 1
                flashed[fx[k], fy[k]] = 1
                changed = True
    return np.where(flashed > 0, 0, arr), np.sum(flashed)


total = 0
for _ in range(100):
    octopuses, n_flashes = step(octopuses)
    total += n_flashes
print(total)


octopuses = np.array([[int(c) for c in l] for l in lines], dtype=int)
k = 0
n_flashes = 0
while n_flashes < np.size(octopuses):
    octopuses, n_flashes = step(octopuses)
    k += 1
print(k)
