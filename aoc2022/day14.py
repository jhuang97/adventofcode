import matplotlib.pyplot as plt
import numpy as np

file1 = open('day14_in.txt', 'r')
# file1 = open('day14_test.txt', 'r')
lines = file1.read().strip().splitlines()

paths = []
for l in lines:
    pts = l.split(' -> ')
    arr = np.zeros((len(pts), 2), dtype=int)
    for k, pt in enumerate(pts):
        parts = pt.split(',')
        arr[k, 0] = int(parts[0])
        arr[k, 1] = int(parts[1])
    paths.append(arr)
    # print(arr)

# print(paths)
path_all = np.vstack(tuple(paths))
xmin = np.min(path_all[:, 0])
xmax = np.max(path_all[:, 0])
ymax = np.max(path_all[:, 1])


def get_grid(nr, nc, xmin, paths):
    grid = np.zeros((nr, nc), dtype=int)
    # print(grid.shape)
    for path in paths:
        for p1, p2 in zip(path, path[1:]):
            c1 = min(p1[0], p2[0]) - xmin
            c2 = max(p1[0], p2[0])+1 - xmin
            r1 = min(p1[1], p2[1])
            r2 = max(p1[1], p2[1])+1
            grid[r1:r2, c1:c2] = 1
    return grid


def try_fall(grid, rs, cs):
    for dr, dc in [(1,0), (1,-1), (1,1)]:
        rs2, cs2 = rs+dr, cs+dc
        if grid[rs2, cs2] == 0:
            return rs2, cs2


nr, nc = ymax+1, xmax-xmin+1
grid = get_grid(nr, nc, xmin, paths)

ri, ci = 0, 500-xmin
count = 0
done = False
while not done:
    rs, cs = ri, ci
    while True:
        if rs >= nr-1 or cs < 0 or cs >= nc:
            done = True
            break
        fall = try_fall(grid, rs, cs)
        if fall is not None:
            rs, cs = fall
        else:
            grid[rs, cs] = 2
            count += 1
            break

print(count)
# plt.imshow(grid)
# plt.show()

ymax2 = ymax + 2
margin = 10
xc = 500
xmin2 = xc - ymax2 - margin
xmax2 = xc + ymax2 + margin
nr2, nc2 = ymax2+1, xmax2-xmin2+1
grid2 = get_grid(nr2, nc2, xmin2, paths)
grid2[-1, :] = 1

ri, ci = 0, 500-xmin2
count2 = 0
done = False
while not done:
    rs, cs = ri, ci
    while True:
        if grid2[ri, ci] > 0:
            done = True
            break
        fall = try_fall(grid2, rs, cs)
        if fall is not None:
            rs, cs = fall
        else:
            grid2[rs, cs] = 2
            count2 += 1
            break

print(count2)
fig = plt.figure()
ax1 = plt.subplot2grid((1,5), (0,0))
ax2 = plt.subplot2grid((1,5), (0,1), colspan=4)
ax1.imshow(grid)
ax2.imshow(grid2)
ax1.axis('off')
ax2.axis('off')

# plt.tight_layout()
plt.show()