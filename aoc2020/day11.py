import copy
import numpy as np

def pad(amap):
    h = len(amap)
    w = len(amap[0])
    return [['.'] * (w+2)] + [(['.'] + l + ['.']) for l in amap] + [['.'] * (w+2)]


def pad2(is_occ):
    h = is_occ.shape[0]
    w = is_occ.shape[1]
    new_arr = np.zeros((h+2, w+2), dtype=is_occ.dtype)
    new_arr[1:h+1, 1:w+1] = is_occ
    return new_arr


file1 = open('day_11_input.txt', 'r')
seat_map = [list(l) for l in file1.read().splitlines()]
seat_map2 = pad(seat_map)
seat_map2 = np.array(seat_map2)

is_chair = (seat_map2 == 'L').astype(int)
is_occ = np.zeros(is_chair.shape, dtype=int)


def step(is_occ, is_chair):
    h = is_occ.shape[0]
    w = is_occ.shape[1]
    occ_total = np.array([is_occ[1+j:h-1+j, 1+i:w-1+i] for j in [-1, 0, 1] for i in [-1, 0, 1] if (j != 0 or i != 0)]).sum(axis=0)
    occ_total = pad2(occ_total)

    next_occ = (is_occ == 0).astype(int) * (occ_total == 0).astype(int) + (is_occ == 1).astype(int) * (occ_total < 4).astype(int)
    next_occ *= is_chair
    return next_occ


while True:
    next_occ = step(is_occ, is_chair)
    if np.array_equal(is_occ, next_occ):
        break
    is_occ = next_occ

print(np.sum(is_occ))


def find_visible(is_chair):
    h = is_chair.shape[0]
    w = is_chair.shape[1]
    visible = dict()
    for y in range(h):
        for x in range(w):
            if is_chair[y, x] == 1:
                vlist = []
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx != 0 or dy != 0:
                            y2 = y + dy
                            x2 = x + dx
                            while 0 <= y2 < h and 0 <= x2 < w:
                                if is_chair[y2, x2] == 1:
                                    vlist.append((y2, x2))
                                    break
                                y2 += dy
                                x2 += dx
                if vlist:
                    visible[(y,x)] = copy.deepcopy(vlist)
    return visible


visible_chairs = find_visible(is_chair)


def step2(is_occ, is_chair, visible_chairs):
    h = is_occ.shape[0]
    w = is_occ.shape[1]
    occ_total = np.zeros(is_occ.shape, dtype=int)
    for y in range(h):
        for x in range(w):
            if (y,x) in visible_chairs:
                for y2, x2 in visible_chairs[y, x]:
                    if is_occ[y2, x2] == 1:
                        occ_total[y,x] += 1
    next_occ = (is_occ == 0).astype(int) * (occ_total == 0).astype(int) + (is_occ == 1).astype(int) * (occ_total < 5).astype(int)
    next_occ *= is_chair
    return next_occ


# print(visible_chairs)
is_occ = np.zeros(is_chair.shape, dtype=int)
while True:
    next_occ = step2(is_occ, is_chair, visible_chairs)
    # print(next_occ)
    if np.array_equal(is_occ, next_occ):
        break
    is_occ = next_occ

print(np.sum(is_occ))