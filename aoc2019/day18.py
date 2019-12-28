import copy

dirs = [(0,1), (0,-1), (-1,0), (1,0)]

def in_bounds(pt, ship_map):
    ysize = len(ship_map)
    xsize = len(ship_map[0])
    return pt[0] >= 0 and pt[0] < xsize and pt[1] >= 0 and pt[1] < ysize

def get(ship_map, pt):
    # if not in_bounds(pt, ship_map):
    #     return None
    return ship_map[pt[1]][pt[0]]

def list_keys(raw_map):
    key_list = []
    for k in raw_map:
        for c in k:
            if c.islower():
                key_list.append(c)
    key_list.sort()
    return key_list

# find nearest keys using DFS
# return dicts of key locations and distances
def nearest_keys(raw_map, start_pos):
    dist_to_start = {start_pos: 0}

    cur_dist = 0
    cur_dist_pts = {start_pos}
    next_pts = set()
    key_locs = {}
    key_dist = {}
    while len(cur_dist_pts) > 0:
        for pt in cur_dist_pts:
            for d in dirs:
                new_pos = (pt[0] + d[0], pt[1] + d[1])
                if in_bounds(new_pos, raw_map):
                    new_val = get(raw_map, new_pos)
                    if new_pos not in dist_to_start and (new_val == '.' or new_val == '@'):
                        next_pts.add(new_pos)
                    if new_val.islower():
                        if new_val not in key_locs or key_dist[new_val] > cur_dist+1:
                            key_locs[new_val] = new_pos
                            key_dist[new_val] = cur_dist+1
        for pt in next_pts:
            dist_to_start[pt] = cur_dist+1
        cur_dist_pts = next_pts
        next_pts = set()
        cur_dist += 1

    return key_locs, key_dist

# find nearest keys using DFS
# return dicts of key locations and distances, except now map is divided into 4 sections and you have 4 robots
def nearest_keys4(raw_map, q_dict, start_pos_list):
    key_locs_all = {}
    key_dist_all = {}

    for qidx in range(4):
        start_pos = start_pos_list[qidx]
        dist_to_start = {start_pos: 0}

        cur_dist = 0
        cur_dist_pts = {start_pos}
        next_pts = set()
        key_locs = {}
        key_dist = {}
        while len(cur_dist_pts) > 0:
            for pt in cur_dist_pts:
                for d in dirs:
                    new_pos = (pt[0] + d[0], pt[1] + d[1])
                    if in_bounds(new_pos, raw_map):
                        new_val = get(raw_map, new_pos)
                        if new_pos not in dist_to_start and (new_val == '.' or new_val == '@'):
                            next_pts.add(new_pos)
                        if new_val.islower():
                            if new_val not in key_locs or key_dist[new_val] > cur_dist+1:
                                key_locs[new_val] = (new_pos, qidx)
                                key_dist[new_val] = cur_dist+1
            for pt in next_pts:
                dist_to_start[pt] = cur_dist+1
            cur_dist_pts = next_pts
            next_pts = set()
            cur_dist += 1

        key_locs_all.update(key_locs)
        key_dist_all.update(key_dist)

    # print(len(key_locs_all))
    # print(key_locs_all)
    return key_locs_all, key_dist_all

def shortest_helper4(memo, raw_map, q_dict, keys_remaining, start_pos_list):
    if len(keys_remaining) == 0:
        return copy.deepcopy(raw_map), 0, [], start_pos_list
    kr_str = "".join(keys_remaining)
    pos_tuple = (start_pos_list[0][0], start_pos_list[0][1], start_pos_list[1][0], start_pos_list[1][1], start_pos_list[2][0], start_pos_list[2][1], start_pos_list[3][0], start_pos_list[3][1])
    if (kr_str, pos_tuple) in memo:
        return memo[(kr_str, pos_tuple)]

    key_locs, key_dist = nearest_keys4(raw_map, q_dict, start_pos_list)
    min_dist = 10000000000
    best_key = None
    best_keys_remaining = None
    best_map = raw_map
    best_pos_list = [(-1, -1),(-1, -1),(-1, -1),(-1, -1)]
    for k in key_locs.keys():
        new_keys_remaining = copy.deepcopy(keys_remaining)
        new_keys_remaining.remove(k)
        next_pos, q_idx = key_locs[k]
        next_pos_list = copy.deepcopy(start_pos_list)
        next_pos_list[q_idx] = next_pos
        end_map, next_dist, next_keys_remaining, end_pos_list = shortest_helper4(memo, use_key(raw_map, k), q_dict, new_keys_remaining, next_pos_list)
        total_dist = next_dist + key_dist[k]
        if total_dist < min_dist:
            min_dist = total_dist
            best_key = k
            best_keys_remaining = next_keys_remaining
            best_map = end_map
            best_pos_list = end_pos_list

    memo[(kr_str, pos_tuple)] = (best_map, min_dist, best_keys_remaining, best_pos_list)
    if len(memo) % 100 == 0:
        print(len(memo))
    return best_map, min_dist, best_keys_remaining, best_pos_list

def shortest4(raw_map, q_dict, start_pos_list):
    key_list = list_keys(raw_map)
    memo = {}
    end_map, total_dist, end_keys_remaining, end_pos_list = shortest_helper4(memo, raw_map, q_dict, key_list, start_pos_list)
    return total_dist

def shortest_helper3(memo, raw_map, keys_remaining, start_pos):
    if len(keys_remaining) == 0:
        return copy.deepcopy(raw_map), 0, copy.deepcopy(keys_remaining), start_pos
    kr_str = "".join(keys_remaining)
    if (kr_str, start_pos) in memo:
        return memo[(kr_str, start_pos)]

    key_locs, key_dist = nearest_keys(raw_map, start_pos)

    min_dist = 10000000000
    best_key = None
    best_keys_remaining = None
    best_map = raw_map
    best_pos = (-1, -1)
    for k in key_locs.keys():
        new_keys_remaining = copy.deepcopy(keys_remaining)
        new_keys_remaining.remove(k)
        next_pos = key_locs[k]
        end_map, next_dist, next_keys_remaining, end_pos = shortest_helper3(memo, use_key(raw_map, k), new_keys_remaining, next_pos)
        total_dist = next_dist + key_dist[k]
        if total_dist < min_dist:
            min_dist = total_dist
            best_key = k
            best_keys_remaining = next_keys_remaining
            best_map = end_map
            best_pos = end_pos

    memo[(kr_str, start_pos)] = (best_map, min_dist, best_keys_remaining, best_pos)
    if len(memo) % 100 == 0:
        print(len(memo))
    return best_map, min_dist, best_keys_remaining, best_pos

def shortest3(raw_map, start_pos):
    key_list = list_keys(raw_map)
    memo = {}
    end_map, total_dist, end_keys_remaining, end_pos = shortest_helper3(memo, raw_map, key_list, start_pos)
    return total_dist

def shortest_helper2(raw_map, keys_remaining, start_pos):
    key_locs, key_dist = nearest_keys(raw_map, start_pos)
    if len(key_locs) == 0:
        return copy.deepcopy(raw_map), 0, copy.deepcopy(keys_remaining), start_pos

    min_dist = 10000000000
    best_key = None
    best_keys_remaining = None
    best_map = raw_map
    best_pos = (-1, -1)
    for k in key_locs.keys():
        new_keys_remaining = copy.deepcopy(keys_remaining)
        new_keys_remaining.remove(k)
        next_pos = key_locs[k]
        end_map, next_dist, next_keys_remaining, end_pos = shortest_helper2(use_key(raw_map, k), new_keys_remaining, next_pos)
        total_dist = next_dist + key_dist[k]
        if total_dist < min_dist:
            min_dist = total_dist
            best_key = k
            best_keys_remaining = next_keys_remaining
            best_map = end_map
            best_pos = end_pos

    return best_map, min_dist, best_keys_remaining, best_pos

def shortest2(raw_map, start_pos):
    key_list = list_keys(raw_map)
    end_map, total_dist, end_keys_remaining, end_pos = shortest_helper2(raw_map, key_list, start_pos)
    return total_dist

def shortest_helper(raw_map, dist_so_far, keys_so_far, start_pos):
    key_locs, key_dist = nearest_keys(raw_map, start_pos)

    if len(key_locs) == 0:
        print('we at distance %d at (%d,%d); used %s, choosing between %s' % ((dist_so_far,) + start_pos + ("".join(keys_so_far), "".join(key_locs.keys()))))
        return copy.deepcopy(raw_map), dist_so_far, copy.deepcopy(keys_so_far), start_pos
    min_dist = 10000000000
    best_keys_so_far = None
    best_pos = (-1,-1)
    best_map = raw_map
    for k in key_locs.keys():
        new_keys_so_far = copy.deepcopy(keys_so_far)
        new_keys_so_far.append(k)
        next_pos = key_locs[k]
        end_map, total_dist, end_keys_so_far, end_pos = shortest_helper(use_key(raw_map, k), dist_so_far + key_dist[k], new_keys_so_far, next_pos)
        if total_dist < min_dist:
            min_dist = total_dist
            best_keys_so_far = end_keys_so_far
            best_pos = end_pos
            best_map = end_map
            # if len(end_keys_so_far) < 9:
            #     print_map(end_map)

    return best_map, min_dist, best_keys_so_far, best_pos

def shortest(raw_map, start_pos):
    end_map, total_dist, end_keys_so_far, end_pos = shortest_helper(raw_map, 0, [], start_pos)
    return total_dist, end_keys_so_far

def find_one(raw_map, to_find):
    for yidx in range(len(raw_map)):
        for xidx in range(len(raw_map[0])):
            if raw_map[yidx][xidx] == to_find:
                return (xidx, yidx)
    return None

def use_key(raw_map, key):
    new_raw_map = copy.deepcopy(raw_map)
    for yidx in range(len(raw_map)):
        for xidx in range(len(raw_map[0])):
            if raw_map[yidx][xidx] == key or raw_map[yidx][xidx] == key.upper():
                new_raw_map[yidx][xidx] = '.'
    return new_raw_map

def print_map(map_arr):
    for k in map_arr:
        print("".join(k))

def map_str_to_arr(raw_map):
    return [list(s) for s in raw_map.split('\n')]

def get_quadrant_dict(raw_map, pos):
    qidx = 0
    q_dict = {}
    for dx in [-1, 1]:
        for dy in [-1, 1]:
            map_arr[yc+dy][xc+dx] = '@'
            for pos in dfs_flood_fill(raw_map, (xc+dx, yc+dy)):
                q_dict[pos] = qidx
            qidx += 1
    return q_dict

def dfs_flood_fill(raw_map, pos):
    frontier = [pos]
    explored = []
    while len(frontier) > 0:
        next_pt = frontier.pop()
        for d in dirs:
            new_pos = (next_pt[0] + d[0], next_pt[1] + d[1])
            val = raw_map[new_pos[1]][new_pos[0]]
            if val.isupper() or val.islower() or val == '.' or val == '@':
                if new_pos not in explored and new_pos not in frontier:
                    frontier.append(new_pos)
        explored.append(next_pt)
    return explored


if __name__ == '__main__':
    raw_map = """########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################"""
    raw_map = """########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################"""
    raw_map = """#############
#DcBa.#.GhKl#
#.###...#I###
#e#d#.@.#j#k#
###C#...###J#
#fEbA.#.FgHi#
#############"""
    raw_map = """#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba@#@BcIJ#
#############
#nK.L@#@G...#
#M###N#H###.#
#o#m..#i#jk.#
#############"""
    raw_map = """#################################################################################
#.........#.............#.......#.....#.#.....................#...#..c#.........#
#.###.#####.#######.#####.###.#.#.###.#.#.#######.###########.#.#.###.#.#####.#.#
#.#.#.#e..#...#.#...#.....#.#.#...#.....#..b#...#.#.........#...#.....#.#.T..r#.#
#.#.#.#.#.###.#.#.#.#.#####.#.#############.#.###.#.#####.#.#.#######.#.#.#######
#.#...#.#...#...#.#.#.#.....#.........K.#.#.#...#.#.#...#.#...#...#...#.#.......#
#.###.#.###.#.###.#.#.#.###.###########.#.#.###.#.###.#.#.#####.#.#.###.#######.#
#...#.#...#...#...#.#...#.#...#.....#...#.#.#...#.....#.#.#.....#.#...#.#.#.....#
###.#.###.#####.#########.###.#.###.#.#.#.#.#.#.#######.#.#O#####.#####.#.#.###.#
#...#.#.#...#.#.............#.#.#...#.#.#...#x#.#.....#.#.#...#z#.....#.#.#.#...#
#.###.#R###.#.#####.#.#######.#.#.###.#.#.###.#.#.###.#.#.###.#.#####.#.#.#.#####
#.#...#...#.#.....#.#.#.....#.#.#.#...#.#...#.#...#...#.#.#.......#...#...#.....#
#.#.#####.#.###.#.#.#.#.###.#.#.#.#.#######.#.#####L###.#.#.#####.#.#####.#####.#
#.#.......#...#.#.#.#.#...#...#.#.#...Y.#.#.#...#.....#.#.#.#...#.#.......#....q#
#.###########.#.#.#.#####.#######.#####.#.#.###.#######.###.#.#.#.#########.###.#
#...#.......#.#.#.#...#...#..h..#.....#.#.......#.....#...#.#.#.#.#.......#.#...#
#.#.#.#####.#.#.#.###.#.###.###.###.###.#######.#.###.###.#.#.#.#.#.#######.#.###
#.#.....#...#.#.#...#.#.#...#.....#.#...#...#...#...#...#...#.#.#.#.#.......#.#.#
#########.###.#####.#.#.#F#.#####.#.#.###.#.###.###.###.#.###.#.#.#.#.#######.#.#
#.........#...#.....#...#.#.#...#...#.#s#.#...#.#...#...#.#...#.#.#.#.#...#...#.#
#.#####.###.###.#.#####.#.###.#.###.#.#.#.###.###.###.#####.###.#.#.#.#.###.###.#
#..d#...#...#...#.#...#...#...#.#...#.#.#.#.#.....#.#.......#...#...#.#...#.#...#
#.#.#####.###.#.###.#######.###.#####.#.#.#.#######.#############.###.#.#.#.###.#
#.#.....#...#.#...#.........#.#.......#.#.......#.....#.....#.....#...#.#.#.....#
#.#####.###.#####.###########.#########.#######.#.###.###.#.#####.#.#####.#####.#
#.#...#...#...#...#.......#...........#.#.....#...#...#...#.....#.#...#.....#...#
#.#.###.#.###.#.#.#.#####.###.#######.#.#.###.#####.###.#######.#####.#.#####.###
#.#.#...#.#.#.#.#...#.....#...#.......#.#.#.#.....#...#.#.....#.#.....#.........#
#.#.#.###.#.#.#.#####.#####.#####.#####.#.#.###.#.###.#.#.#.###.#.#.#######.#####
#...#.#.#...#.#...#.#.#...#.....#.#.....#.....#.#...#...#.#.#...#.#j#.....#.#.W.#
#####.#.###.#.###.#.#.#.#.#####.#.###.#.#####.#.#########.###.###.###.###.###.#.#
#...#.#.....#.#...#.#.#.#.......#.....#.#.#...#.........#.....#.....#...#...#.#.#
#.#.#.#####.#.#.###.#.#.###############.#.#.#########.###.#########.#.#####.#.#.#
#.#...#...#.#.#w..#...#...#...........#.#.#.#.......#...#...#.....#...#.V.#...#.#
#.#####.#.###.###.#.###.#.#.###########.#.#.#####.#.###.###.###.#M#####.#.#####.#
#.....#.#...#.....#.#.#.#.#.A.#...#.....#.#.......#...#...#...#.#.......#.......#
#####.#.###.#######.#.#.#.#.#.#.#.#.#####.###########.###.###.#.###############.#
#.....#.#.#.......#.#...#.#.#...#.#.....#...#.......#.#.#.#...#.....#.#.....#...#
#.#####.#.#######.#.#####.#.#####.#####.#.#.#.###.###.#.#.#.#######.#.#.###.#.###
#............v..#.........#.....#.........#.....#.......#...........#.....#.....#
#######################################.@.#######################################
#.#.....G.....#.....#.......#.........#.........#.......#...........#.......#...#
#.#.###.#####.#####.#.#####.#.###.###.#.#.#####.#####.#.#######.###.#.###.#.###.#
#.#.#.#.....#.......#.#...#...#.#.#.....#.#...#......a#.......#...#.#.#...#.#...#
#.#.#.#####.#######.#.#.#.#####.#.#####.#.#.#.###############.###.#.#.#.###.#.#.#
#.#..n....#.#.......#.#.#...#...#.....#.#.#.#...#.....#.....#...#.#...#...#.#.#.#
#.#######.#.#########.#.###.#.#######.#.#.#.#####.#.###.#.#.###.#########P#.#.###
#...#.#...#...#u..#...#.#...#.......#.#.#.#...#...#.....#.#...#.....#...#.#.#...#
#.#.#.#.#####.#.#.#.###.###.###.###.#.#.#.###.#.#########.###.#####.#.#U#.#.###.#
#.#...#p..#.#...#...#.....#.....#...#.#.#...#.#.#.....#...#...#...#...#.#.#...#.#
#.###.###.#.###########.#.###########.#####.#.#.###.#.#.###.###.#.#####.#.###.#.#
#...#.#...#...#.......#.#.#..k..#...#...#...#.#.#...#.#.#...#...#...#...#...#.#.#
#.#.###.###.#.###.###.###.#.###.#.#.###.#.###.#.#.###C#Z###.#.#####.#.###.#.#.#.#
#.#.........#.....#.#.#...#.#...#.#...#.#...#.#.#.#...#...#.#.....#.#...#.#.#.#.#
#.#################.#.#.###.#.###.###.#.#.#.#.#.#.#.#####.#.###.###.###.###.#.#.#
#m....#...........#.#...#...#...#...#.#.#.#.#.#.#.#.#.....#...#.#...#..g#.N.#...#
#.#####.#########.#.###.#.#####.###.#.#.###.#.#.#B#.#.#########.#.###.###.#####.#
#.#.....#.....#...#.....#.#...#.#...#...#...#.....#.#.......#...#...#...#.#i..#.#
###.#######.###.#########.#.###.#.#######.#########.#######.#.#####.###.#.#.#.#.#
#...#.......#...#....y....#...#.#.#.....#.#...S.#...#.....#.......#.#...#.#.#.#.#
#.###.#####.#.#.#.#########.#.#.#.#.###.#.#.###.#.###.###.#####.###.#.###.#.#.#.#
#...#.#.#...#.#.#.....#...#.#...#.....#.#.....#.#...#.#.....#.#.#...#.....#.#.#.#
###.#.#.#.###.#########.#.#.#####.#####.#######.###X#.#######.###.#.#######.###.#
#...#.#.#...#...........#.#...#...#.....#...#...#...#.#.......#...#.....#.......#
#Q###.#.###.#####.###########.#.###.###.#.#.#.#####.#.#.#######.#########.#######
#.....#...#.#...#.........#...#.#...#.#.#.#.#.....#...#...#.....#.......#.......#
#######.###.#.###########.#.#####.###.#.#.#.#####.###.###.#####.#D#####.#######.#
#.....#...#.#.......#...#...#.....#.....#.#.#...#.#....l#...#...#.#...#.......#.#
###.#.###.#.###.###.###.#####.#.#########.#.#.###.#########.#.#.#.###.#######.#.#
#...#...#.#.....#...#.......#.#.........#.#.#.#...#...#...#.#.#.#...#.......#...#
#.#####.#.#######.###.#######.#########.#.#.#.#.###.#.#.#.#.#.#.###.#.#####.#####
#.#..t#.#.....#...#.............#.....#.#.#.#.#.....#...#...#.#.#...#.#...#.....#
#.###.#.#.#####.###.###########.#.#.###.#.#.#.###############.#.#.#####.#.#####.#
#...#.....#...#.#.....#.......#...#.#...#.#.........#.........#.#.......#.#.....#
#E#.#.#####.#.#.#####.#.#####.#####.#.###.###.#######.#####.#############.#.#####
#.#.#...#...#.#...#...#.#...#...#...#...#...#.#.....#.#...#.........#.....#.#...#
###.#####.###I###.#.###.#.#.###.#####.#.#.#.###.###.#.#.#######.#####.#####.#.#.#
#...#...#...#...#.#.#...#.#...#.#...#.#.#.#..f..#.#...#.....#...#.....#...#...#.#
#.###.#.###.#.###.###.###.#####.#.#.###.#.#######.#########.#.###.#####.#.#####.#
#.J...#.....#.........#...........#.....#.............H....o#...........#.......#
#################################################################################"""

    map_arr = map_str_to_arr(raw_map)

    start_loc = find_one(map_arr, '@')
    key_locs, key_dist = nearest_keys(map_arr, start_loc)

    print(start_loc)
    print(list_keys(map_arr))
    print(key_locs)
    print(key_dist)

    # total_dist, key_order = shortest(map_arr, start_loc)
    # print('total distance = %d' % total_dist)
    # print(key_order)

    # print('shortest dist is %d' % shortest3(map_arr, start_loc))

    # END PART 1 START PART 2

    print(len(map_arr))
    print(len(map_arr[0]))
    yc = len(map_arr)//2
    xc = len(map_arr[0])//2
    map_arr[yc][xc] = '#'
    for d in dirs:
        map_arr[yc+d[1]][xc+d[0]] = '#'
    start_locs = []
    for dx in [-1, 1]:
        for dy in [-1, 1]:
            map_arr[yc+dy][xc+dx] = '@'
            start_locs.append((xc+dx, yc+dy))

    for k in map_arr:
        print("".join(k))

    print(start_locs)
    q_dict = get_quadrant_dict(map_arr, start_locs)
    # print(q_dict)

    print('shortest dist is %d' % shortest4(map_arr, q_dict, start_locs))
