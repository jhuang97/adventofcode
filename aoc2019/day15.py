def numparam(opcode):
    numparamvals = [1, 3, 3, 1, 1, 2, 2, 3, 3, 1]
    if opcode <= len(numparamvals) and opcode >= 1:
        return numparamvals[opcode]
    elif opcode == 99:
        return 0
    return 0

class IntComp:
    def __init__(self, codes, inputval):
        self.codes = codes
        # self.phase = phase
        self.inputval = inputval
        self.first_input = True
        self.idx = 0
        self.msize = len(codes)
        self.extra_memory = {}
        self.rbase = 0
        # print("msize = %d" % self.msize)

    def set(self, mloc, val):
        if mloc < self.msize and mloc >= 0:
            self.codes[mloc] = val
        elif mloc >= self.msize:
            self.extra_memory[mloc] = val
        elif mloc < 0:
            print("negative memory address")

    def get(self, mloc):
        if mloc < self.msize and mloc >= 0:
            return self.codes[mloc]
        elif mloc in self.extra_memory:
            return self.extra_memory[mloc]
        else:
            return 0

    def run(self, iv2):
        self.inputval = iv2
        while True:
            # print("idx = %d, extra_memory_size %d" % (self.idx, len(self.extra_memory)))
            mcode = self.get(self.idx)
            opcode = mcode % 100
            pmodes = [mcode//100%10, mcode//1000%10, mcode//10000%10]
            pvals = [None, None, None]
            pidx = [None, None, None]
            nparams = numparam(opcode)
            if nparams > 0:
                for i in range(nparams):
                    if pmodes[i] == 0 or pmodes[i] == 2: # position
                        pidx[i] = self.get(self.idx+i+1)
                        if pmodes[i] == 2:
                            pidx[i] = pidx[i] + self.rbase
                        pvals[i] = self.get(pidx[i])
                        
                        # pvals[i] = self.codes[self.codes[self.idx+i+1]]
                        # if self.codes[self.codes[self.idx+i+1]] != self.get(self.get(self.idx+i+1)):
                        #     print("%d not %d" % (self.codes[self.codes[self.idx+i+1]], self.get(self.get(self.idx+i+1))))
                    elif pmodes[i] == 1: # immediate
                        pvals[i] = self.get(self.idx+i+1)
                        pidx[i] = self.get(self.idx+i+1)
                        # pvals[i] = self.codes[self.idx+i+1]

            # print("opcode %d" % opcode)
            # print(pmodes)
            # print(pvals)
            # print(pidx)
            if opcode == 1:
                self.set(pidx[2], pvals[0] + pvals[1])
                # self.set(self.get(self.idx+3), pvals[0] + pvals[1])
                # self.codes[self.codes[self.idx+3]] = pvals[0] + pvals[1]
                self.idx = self.idx + 4
            elif opcode == 2:
                self.set(pidx[2], pvals[0] * pvals[1])
                # self.set(self.get(self.idx+3), pvals[0] * pvals[1])
                self.idx = self.idx + 4
            elif opcode == 3:
                # if self.first_input:
                #     self.set(pidx[0], self.phase)
                #     self.first_input = False
                # else:
                self.set(pidx[0], self.inputval)
                    # self.codes[self.codes[self.idx+1]] = self.inputval
                self.idx = self.idx+2
            elif opcode == 4:
                # print('OUTPUT:')
                # print(pvals[0])
                self.idx=self.idx+2
                return pvals[0]
                
            elif opcode == 5:
                if pvals[0] != 0:
                    self.idx = pvals[1]
                else:
                    self.idx = self.idx+3
            elif opcode == 6:
                if pvals[0] == 0:
                    self.idx = pvals[1]
                else:
                    self.idx = self.idx+3
            elif opcode == 7:
                if pvals[0] < pvals[1]:
                    self.set(pidx[2], 1)
                    # self.codes[self.codes[self.idx+3]] = 1
                else:
                    self.set(pidx[2], 0)
                    # self.codes[self.codes[self.idx+3]] = 0
                self.idx = self.idx+4
            elif opcode == 8:
                if pvals[0] == pvals[1]:
                    self.set(pidx[2], 1)
                    # self.codes[self.codes[self.idx+3]] = 1
                else:
                    self.set(pidx[2], 0)
                    # self.codes[self.codes[self.idx+3]] = 0
                self.idx = self.idx+4
            elif opcode == 9:
                self.rbase = self.rbase + pvals[0]
                self.idx = self.idx+2
            elif opcode == 99:
                return -100000

dir_commands = {(0,1):1, (0,-1):2, (-1,0):3, (1,0):4}
dirs = [(0,1), (0,-1), (-1,0), (1,0)]

def travel_to(curr_pos, dest, ic, ship_map):
    if curr_pos == dest:
        return 0

    route = calculate_route(curr_pos, dest, ship_map)
    if len(route) <= 1:
        return -1

    route_commands = get_route_commands(route)
    for c in route_commands:
        res = ic.run(c)
        if res == 0:
            print('bad route, ran into a wall')
            return -2
    return 0

# calculate route only using known map
def calculate_route(start, dest, ship_map):
    cur_pos = start
    if cur_pos == dest:
        return [dest]

    if ship_map[dest] == 0:
        return [start]
    if ship_map[start] == 0:
        return [dest]

    dists = {}
    prevs = {}
    unexplored = []
    dists[cur_pos] = 0
    unexplored.append(cur_pos)
    while len(unexplored) > 0:
        next_pt = unexplored.pop(0)
        if next_pt != start:
            prev = prevs[next_pt]
            dists[next_pt] = dists[prev]+1
            if next_pt == dest:
                break
        
        to_explore = []
        for d in dirs:
            new_pt = (next_pt[0] + d[0], next_pt[1] + d[1])
            if new_pt in ship_map and ship_map[new_pt] != 0:
                to_explore.append(new_pt)
        for nn in to_explore:
            if nn not in dists and nn not in unexplored:
                unexplored.append(nn)
                prevs[nn] = next_pt

    route_pts = [dest]
    ptr = prevs[dest]
    while ptr != start:
        route_pts.insert(0, ptr)
        ptr = prevs[ptr]
    route_pts.insert(0, start)

    return route_pts

def get_route_commands(route):
    if len(route) < 2:
        return []
    commands = []
    for idx in range(1, len(route)):
        disp = (route[idx][0] - route[idx-1][0], route[idx][1] - route[idx-1][1])
        if disp in dir_commands:
            commands.append(dir_commands[disp])
        else:
            print('illegal route, must move by exactly one step')
            return commands
    return commands

def find_max_dist(start, ship_map):
    dist_to_start = {start: 0}

    cur_dist = 0
    cur_dist_pts = {start}
    next_pts = set()
    while len(cur_dist_pts) > 0:
        for pt in cur_dist_pts:
            for d in dirs:
                new_pos = (pt[0] + d[0], pt[1] + d[1])
                if new_pos in ship_map and new_pos not in dist_to_start and ship_map[new_pos] != 0:
                    next_pts.add(new_pos)
        for pt in next_pts:
            dist_to_start[pt] = cur_dist+1
        cur_dist_pts = next_pts
        next_pts = set()
        cur_dist += 1

    return cur_dist-1

def bfs_towards_oxygen(ic):
    pos = (0, 0)
    ship_map = {pos:1} # stores map; wall = 0, normal space = 1, oxygen_tank = 2
    dist_to_start = {(0,0): 0}

    cur_dist = 0
    cur_dist_pts = {pos}
    next_pts = set()
    while len(cur_dist_pts) > 0:
        for pt in cur_dist_pts:
            # move robot to point
            if travel_to(pos, pt, ic, ship_map) < 0:
                print('oh no, travel failed')
            pos = pt

            # explore all neighbors
            n_map = check_neighbors(ic)
            for d, val in n_map.items():
                new_pos = (pos[0] + d[0], pos[1] + d[1])
                ship_map[new_pos] = val
                if val == 1 or val == 2:
                    if new_pos not in dist_to_start:
                        next_pts.add(new_pos)
                        if val == 2:
                            print_ship_map(ship_map, pos)
                            return cur_dist+1
        for pt in next_pts:
            dist_to_start[pt] = cur_dist+1
        cur_dist_pts = next_pts
        next_pts = set()
        cur_dist += 1
    return -1

def dfs_explore(ic):
    pos = (0, 0)
    ship_map = {pos:1} # stores map; wall = 0, normal space = 1, oxygen_tank = 2
    oxygen_loc = (0, 0)

    frontier = [pos]
    explored = []
    while len(frontier) > 0:
        next_pt = frontier.pop()
        if travel_to(pos, next_pt, ic, ship_map) < 0:
                print('oh no, travel failed')
        pos = next_pt

        n_map = check_neighbors(ic)
        for d, val in n_map.items():
            new_pos = (pos[0] + d[0], pos[1] + d[1])
            ship_map[new_pos] = val
            if val == 1 or val == 2:
                if new_pos not in explored and new_pos not in frontier:
                    frontier.append(new_pos)
            if val == 2:
                oxygen_loc = new_pos

        explored.append(next_pt)

    return ship_map, oxygen_loc

def check_neighbors(ic):
    n_map = {}
    for d in dirs:
        command = dir_commands[d]
        res = ic.run(command)
        n_map[d] = res
        if res == 1 or res == 2:
            ncommand = dir_commands[(-d[0], -d[1])]
            ic.run(ncommand)
    return n_map

def interactive_intcomp_session(ic):
    pos = (0, 0)
    ship_map = {pos:1} # stores map; wall = 0, normal space = 1, oxygen_tank = 2

    key_dirs = {'d':(1,0), 'a':(-1,0), 's':(0,-1), 'w':(0,1)}

    n_map = check_neighbors(ic)
    for d, val in n_map.items():
        ship_map[(pos[0] + d[0], pos[1] + d[1])] = val

    while True:
        d_in = input("Enter direction (wasd) or fast-travel by typing 'g x y':")
        if d_in in key_dirs:
            d_pos = key_dirs[d_in]
            command = dir_commands[d_pos]
            new_pos = (pos[0] + d_pos[0], pos[1] + d_pos[1])
            res = ic.run(command)
            ship_map[new_pos] = res
            if res == 0: # wall
                pass
            elif res == 1: # move
                pos = new_pos
            elif res == 2: # move; oxygen
                pos = new_pos
        elif d_in[0:1] == 'g':
            coord_text = d_in[2:].split(' ')
            try:
                target_pos = (int(coord_text[0]), int(coord_text[1]))
                route = calculate_route(pos, target_pos, ship_map)
                print_ship_map_with_route(ship_map, pos, route)

                if len(route) > 1:
                    route_commands = get_route_commands(route)
                    print(str(route_commands))
                    for c in route_commands:
                        res = ic.run(c)
                        if res == 0:
                            print('bad route, ran into a wall')

                    pos = target_pos

            except (ValueError, IndexError) as e:
                print('bad input: ' + coord_text)
        
        n_map = check_neighbors(ic)
        for d, val in n_map.items():
            ship_map[(pos[0] + d[0], pos[1] + d[1])] = val

        print_ship_map(ship_map, pos)

def print_ship_map(ship_map, pos):
    x1 = 10000
    x2 = -10000
    y1 = 10000
    y2 = -10000
    for coords in ship_map.keys():
        x = coords[0]
        if x < x1:
            x1 = x
        if x > x2:
            x2 = x
        y = coords[1]
        if y < y1:
            y1 = y
        if y > y2:
            y2 = y
    out_arr = [['?' for j in range(x2-x1+1)] for i in range(y2-y1+1)]
    obj_chars = ['#', ' ', 'O']
    for coords, val in ship_map.items():
        if coords == pos:
            out_arr[coords[1]-y1][coords[0]-x1] = 'D'
        elif coords == (0, 0):
            out_arr[coords[1]-y1][coords[0]-x1] = '0'
        else:
            out_arr[coords[1]-y1][coords[0]-x1] = obj_chars[val]

    for ri in reversed(range(len(out_arr))):
        print("".join(out_arr[ri]))
    print(str(pos))

def print_ship_map_with_route(ship_map, pos, route):
    x1 = 10000
    x2 = -10000
    y1 = 10000
    y2 = -10000
    for coords in ship_map.keys():
        x = coords[0]
        if x < x1:
            x1 = x
        if x > x2:
            x2 = x
        y = coords[1]
        if y < y1:
            y1 = y
        if y > y2:
            y2 = y
    out_arr = [['?' for j in range(x2-x1+1)] for i in range(y2-y1+1)]
    obj_chars = ['#', ' ', 'O']
    for coords, val in ship_map.items():
        if coords == pos:
            out_arr[coords[1]-y1][coords[0]-x1] = 'D'
        elif coords in route:
            out_arr[coords[1]-y1][coords[0]-x1] = '@'
        elif coords == (0, 0):
            out_arr[coords[1]-y1][coords[0]-x1] = '0'
        else:
            out_arr[coords[1]-y1][coords[0]-x1] = obj_chars[val]

    for ri in reversed(range(len(out_arr))):
        print("".join(out_arr[ri]))
    print(str(pos))

if __name__ == '__main__':
    import copy
    codes = [3,1033,1008,1033,1,1032,1005,1032,31,1008,1033,2,1032,1005,1032,58,1008,1033,3,1032,1005,1032,81,1008,1033,4,1032,1005,1032,104,99,101,0,1034,1039,1001,1036,0,1041,1001,1035,-1,1040,1008,1038,0,1043,102,-1,1043,1032,1,1037,1032,1042,1105,1,124,102,1,1034,1039,1002,1036,1,1041,1001,1035,1,1040,1008,1038,0,1043,1,1037,1038,1042,1106,0,124,1001,1034,-1,1039,1008,1036,0,1041,1002,1035,1,1040,102,1,1038,1043,102,1,1037,1042,1106,0,124,1001,1034,1,1039,1008,1036,0,1041,1001,1035,0,1040,1002,1038,1,1043,101,0,1037,1042,1006,1039,217,1006,1040,217,1008,1039,40,1032,1005,1032,217,1008,1040,40,1032,1005,1032,217,1008,1039,37,1032,1006,1032,165,1008,1040,33,1032,1006,1032,165,1101,0,2,1044,1106,0,224,2,1041,1043,1032,1006,1032,179,1101,0,1,1044,1105,1,224,1,1041,1043,1032,1006,1032,217,1,1042,1043,1032,1001,1032,-1,1032,1002,1032,39,1032,1,1032,1039,1032,101,-1,1032,1032,101,252,1032,211,1007,0,62,1044,1106,0,224,1101,0,0,1044,1106,0,224,1006,1044,247,101,0,1039,1034,1002,1040,1,1035,102,1,1041,1036,101,0,1043,1038,1001,1042,0,1037,4,1044,1106,0,0,60,10,88,42,71,78,10,10,70,23,65,29,47,58,86,53,77,61,77,63,18,9,20,68,45,15,67,3,95,10,14,30,81,53,3,83,46,31,95,43,94,40,21,54,93,91,35,80,9,17,81,94,59,83,49,96,61,63,24,85,69,82,45,71,48,39,32,69,93,11,90,19,78,54,79,66,6,13,76,2,67,69,10,9,66,43,73,2,92,39,12,99,33,89,18,9,78,11,96,23,55,96,49,12,85,93,49,22,70,93,59,76,68,55,66,54,32,34,36,53,64,84,87,61,43,79,7,9,66,40,69,9,76,92,18,78,49,39,80,32,70,52,74,37,86,11,77,51,15,28,84,19,13,75,28,86,3,82,93,15,79,61,93,93,31,87,43,67,44,83,78,43,46,46,12,89,19,85,44,95,65,24,70,93,50,98,72,66,80,23,87,19,97,40,25,9,49,6,81,35,9,52,71,27,63,3,96,94,21,24,48,79,67,72,72,15,85,93,22,95,34,3,63,21,79,9,51,92,45,87,25,41,80,13,88,68,66,18,85,75,39,80,17,54,93,89,65,21,91,73,53,60,69,29,82,99,5,22,65,9,69,61,80,63,38,71,61,61,11,68,30,74,11,26,53,59,97,2,12,74,79,44,73,72,27,17,34,92,26,27,88,66,5,97,34,81,86,30,35,6,64,36,34,65,80,12,90,65,95,21,90,55,43,71,89,56,97,91,27,27,73,80,34,22,48,89,84,35,88,90,47,4,32,77,31,2,82,66,76,43,74,68,56,78,36,59,66,58,75,89,96,51,51,97,34,49,86,70,26,46,89,43,99,97,66,32,51,32,77,33,86,92,56,68,64,39,83,55,25,98,24,56,73,21,98,39,24,67,21,4,76,10,32,91,53,82,37,59,72,63,78,43,67,2,72,69,50,71,19,72,92,51,12,93,61,88,24,84,35,93,30,63,70,7,78,83,42,63,6,25,24,73,76,22,99,68,14,85,14,75,32,88,42,47,97,2,91,97,51,79,12,71,91,7,1,87,82,21,98,63,37,19,85,1,48,77,54,76,12,92,28,91,25,85,88,8,92,32,67,18,56,51,67,58,80,59,77,76,25,7,73,58,72,96,75,15,27,37,23,83,58,68,83,50,67,41,39,89,24,1,83,63,8,64,54,76,50,3,89,97,74,48,15,91,22,37,71,77,9,1,85,38,23,58,10,75,86,72,80,59,24,64,7,63,85,53,61,89,68,7,80,4,68,56,39,66,31,69,6,7,76,88,17,89,42,64,56,11,97,65,64,71,88,61,31,32,53,88,99,55,73,20,90,10,86,32,50,89,53,83,42,80,28,63,98,38,85,72,57,88,23,52,96,77,39,65,88,40,26,91,56,1,94,51,94,24,20,81,74,23,45,72,56,22,84,70,44,50,68,32,98,51,75,3,61,75,59,3,7,98,76,45,78,47,74,60,69,78,54,67,29,63,47,79,72,57,73,44,63,98,6,93,36,20,27,90,77,39,44,64,68,47,48,69,78,29,76,48,1,81,10,67,32,72,47,89,83,18,39,85,65,97,15,59,13,74,29,84,50,80,94,8,27,83,67,43,75,52,96,17,82,29,83,45,85,82,71,76,44,30,10,91,16,7,31,63,2,68,75,46,70,28,93,91,17,13,81,57,93,32,27,65,61,93,11,84,10,66,14,83,14,77,26,77,13,86,21,84,87,87,34,99,69,88,1,74,61,72,54,93,16,76,54,86,63,94,13,79,24,97,0,0,21,21,1,10,1,0,0,0,0,0,0]
    ic = IntComp(copy.deepcopy(codes), 0)
    # print(bfs_towards_oxygen(ic))
    # interactive_intcomp_session(ic)

    ship_map, oxygen_loc = dfs_explore(ic)
    print_ship_map(ship_map, (0, 0))
    print(oxygen_loc)
    print(find_max_dist(oxygen_loc, ship_map))