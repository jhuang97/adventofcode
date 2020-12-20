import math
import numpy as np

file1 = open('day_20_input.txt', 'r')
tile_str = file1.read().split('\n\n')

tiles = dict()
for ts in tile_str:
    tokens = ts.splitlines()
    if tokens:
        tid = int(tokens[0][:-1].split()[1])
        map_str = tokens[1:]
        map_arr = np.zeros((len(map_str), len(map_str[0])), dtype=bool)
        for i in range(len(map_str)):
            for j in range(len(map_str[0])):
                if map_str[i][j] == '#':
                    map_arr[i, j] = 1
        tiles[tid] = map_arr

sq_len = int(round(math.sqrt(len(tiles))))
tile_len = map_arr.shape[0] - 2
# print(map_arr.shape)


def print_img(arr):
    for r in arr:
        rowstr = ''
        for c in r:
            if c:
                rowstr += '#'
            else:
                rowstr += '_'
        print(rowstr)


def get_border(arr, xb, yb):
    if xb == 0:
        if yb == 1:
            return arr[-1, :]
        elif yb == -1:
            return arr[0, :]
    elif yb == 0:
        if xb == 1:
            return arr[:, -1]
        elif xb == -1:
            return arr[:, 0]


def transformations(arr):
    out = []
    for a2 in [arr, np.fliplr(arr)]:
        out.append(a2)
        a3 = a2.copy()
        for k in range(3):
            a3 = np.rot90(a3)
            out.append(a3)
    return out


dirs = [(0, 1), (0, -1), (-1, 0), (1, 0)]


def try_arrange(map_join, idx, inserted_tids):
    y = idx//sq_len
    x = idx % sq_len

    for tid in tiles.keys():
        if tid not in inserted_tids:
            for arr in transformations(tiles[tid]):
                # check if arr fits
                fits = True
                for dy, dx in dirs:
                    y2 = y + dy
                    x2 = x + dx
                    if 0 <= y2 < sq_len and 0 <= x2 < sq_len:
                        if map_join[y2][x2] is not None:
                            if not np.all(get_border(arr, dx, dy) == get_border(map_join[y2][x2][1], -dx, -dy)):
                                fits = False
                if fits:
                    map_join[y][x] = (tid, arr.copy())
                    inserted_tids.add(tid)
                    if idx == sq_len * sq_len - 1:
                        return True
                    if try_arrange(map_join, idx+1, inserted_tids):
                        return True
                    else:
                        map_join[y][x] = None
                        inserted_tids.remove(tid)
    return False


map_join = []
for k in range(sq_len):
    row = []
    for m in range(sq_len):
        row.append(None)
    map_join.append(row.copy())

inserted_tids = set()
try_arrange(map_join, 0, inserted_tids)

prod = 1
for r in [0, -1]:
    for c in [0, -1]:
        prod *= map_join[r][c][0]
print(prod)

combined = np.zeros((sq_len * tile_len, sq_len * tile_len), dtype=bool)
for r in range(sq_len):
    for c in range(sq_len):
        combined[r*tile_len:(r+1)*tile_len, c*tile_len:(c+1)*tile_len] = map_join[r][c][1][1:-1, 1:-1]

sea_monster = '''                  # 
#    ##    ##    ###
 #  #  #  #  #  #   '''
sm2 = [list(l) for l in sea_monster.splitlines()]
sm_set = set()
sm_nr = len(sm2)
sm_nc = len(sm2[0])
for r in range(sm_nr):
    for c in range(sm_nc):
        if sm2[r][c] == '#':
            sm_set.add((r, c))
# print(sm_set)


def sea_monster_count(img):
    sm_coords = set()
    for r in range(img.shape[0]-sm_nr + 1):
        for c in range(img.shape[1]-sm_nc + 1):
            matches = True
            for sm_r, sm_c in sm_set:
                if not img[r + sm_r, c + sm_c]:
                    matches = False
            if matches:
                for sm_r, sm_c in sm_set:
                    sm_coords.add((sm_r+r, sm_c+c))
    return len(sm_coords)


for a in transformations(combined):
    count = sea_monster_count(a)
    if count > 0:
        print(np.sum(a) - count)
