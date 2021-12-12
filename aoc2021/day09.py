import numpy as np

file1 = open('day_9_input.txt', 'r')
lines = file1.read().strip().split('\n')
# lines = """2199943210
# 3987894921
# 9856789892
# 8767896789
# 9899965678""".split('\n')

nums = [[int(c) for c in list(l)] for l in lines]

nr = len(nums)
nc = len(nums[0])

total = 0
dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
low_points = []
for r in range(nr):
    for c in range(nc):
        lower = True
        for dr, dc in dirs:
            r2 = r+dr
            c2 = c+dc
            if 0 <= r2 < nr and (0 <= c2 < nc):
                if nums[r][c] >= nums[r2][c2]:
                    lower = False
                    break
        if lower:
            total += nums[r][c]+1
            low_points.append((r, c))
print(total)

basin_id = -1*np.ones((nr, nc), dtype=int)
for k, pt in enumerate(low_points):
    r, c = pt
    basin_id[r, c] = k


def get_id(basin_id, pt):
    r, c = pt
    return basin_id[r, c]


def neighbors(pt):
    r, c = pt
    return [(r + dr, c + dc) for dr, dc in dirs if (0 <= r + dr < nr) and (0 <= c + dc < nc)]


frontier = set()
for pt in low_points:
    for pt2 in neighbors(pt):
        if get_id(basin_id, pt2) < 0:
            frontier.add(pt2)

changed = True
while changed:
    changed = False
    for pt in frontier:
        r, c = pt
        if nums[r][c] == 9:
            continue
        for pt2 in neighbors(pt):
            if get_id(basin_id, pt2) >= 0:
                downward_id = get_id(basin_id, pt2)
                break
        basin_id[r, c] = downward_id
        frontier.remove(pt)
        for pt3 in neighbors(pt):
            if get_id(basin_id, pt3) < 0:
                frontier.add(pt3)
        changed = True
        break
[unique, counts] = np.unique(basin_id, return_counts=True)
print(np.prod(sorted(counts[unique > -1])[-3:]))
