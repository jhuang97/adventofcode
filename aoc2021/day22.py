import numpy as np

fname = 'day_22_input.txt'
# fname = 'day_22_test.txt'
file1 = open(fname, 'r')
lines = file1.read().strip().splitlines()

steps = []
for l in lines:
    parts = l.split(' ')
    if parts[0] == 'on':
        val = 1
    elif parts[0] == 'off':
        val = 0
    else:
        print('oh no')
    cstr = parts[1].split(',')
    coords = []
    for s in cstr:
        sub = s[2:].split('..')
        coords.append(int(sub[0]))
        coords.append(int(sub[1]))
    steps.append((val, coords.copy()))
# print(steps)

scale = 50

arr = np.zeros((2*scale+1, 2*scale+1, 2*scale+1), dtype=int)

for val, coord in steps:
    if max(coord) <= scale and min(coord) >= -scale:
        c = [n + scale for n in coord]
        arr[c[0]:c[1]+1, c[2]:c[3]+1, c[4]:c[5]+1] = val
    else:
        pass
small_count = np.sum(arr)
print(small_count)


big_idx = -1  # I observe that part 2 regions don't intersect at all with part 1 regions
for k, step in enumerate(steps):
    val, coord = step
    if not (max(coord) <= scale and min(coord) >= -scale):
        big_idx = k
        # print(k)
        break


def intersect(c1, c2):
    for k in range(3):
        if (c1[2*k] > c2[2*k+1]) or (c2[2*k] > c1[2*k+1]):
            return False
    return True


def intersection(c1, c2):
    out = [0, 0, 0, 0, 0, 0]
    for k in range(3):
        out[2*k] = max(c1[2*k], c2[2*k])
        out[2*k+1] = min(c1[2*k+1], c2[2*k+1])
    return out


def volume(c):
    return (c[1]-c[0]+1) * (c[3]-c[2]+1) * (c[5]-c[4]+1)


# shows that there is only one connected component
region_id = {}
for k in range(big_idx, len(steps)):
    region_id[k] = k
for i1 in range(big_idx, len(steps)-1):
    for i2 in range(i1+1, len(steps)):
        if intersect(steps[i1][1], steps[i2][1]) and region_id[i1] != region_id[i2]:
            id2 = region_id[i2]
            # print(i1, i2)
            k_change = [k for k, v in region_id.items() if v == id2]
            for k in k_change:
                region_id[k] = region_id[i1]
# print(region_id)

# failed attempt to generate Mathematica code to cheese part 2
# def cuboid_str(c):
#     return "Cuboid[{%d, %d, %d}, {%d, %d, %d}]" % (c[0], c[2], c[4], c[1]+1, c[3]+1, c[5]+1)
# for k in range(big_idx, len(steps)):
#     val, coord = steps[k]
#     if k == big_idx:
#         print('c = ' + cuboid_str(coord) + ';')
#     else:
#         if val == 1:
#             print('c = RegionUnion[c, ' + cuboid_str(coord) + '];')
#         else:
#             print('c = RegionDifference[c, ' + cuboid_str(coord) + '];')

set_info = {}
region_def = {}
for k in range(big_idx, len(steps)):
    val, coord = steps[k]
    region_def[(k,)] = coord
    new_set_info = []
    if val == 1:
        new_set_info.append(((k,), 1))
    for reg, coeff in set_info.items():
        if intersect(region_def[(k,)], region_def[reg]):
            new_reg = tuple(sorted(list(set((k,) + reg))))
            region_def[new_reg] = intersection(region_def[(k,)], region_def[reg])
            # print(new_reg)
            new_set_info.append((new_reg, -coeff))  # amazingly, no matter if the new region turns lights on or off,
                                                    # the principle of inclusion/exclusion makes us do the same thing
            # if val == 1:
            #     if coeff == 1:
            #         new_set_info.append((new_reg, -1))
            #     elif coeff == -1:
            #         new_set_info.append((new_reg, 1))
            # elif val == 0:
            #     if coeff == 1:
            #         new_set_info.append((new_reg, -1))
            #     elif coeff == -1:
            #         new_set_info.append((new_reg, 1))
    if new_set_info:
        for reg, coeff in new_set_info:
            set_info[reg] = coeff
        # print(set_info)

big_count = 0
for reg, coeff in set_info.items():
    big_count += coeff * volume(region_def[reg])
print(big_count + small_count)