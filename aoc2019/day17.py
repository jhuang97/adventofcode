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
        self.use_in_buffer = False
        self.in_buffer = []
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
                if self.use_in_buffer:
                    self.set(pidx[0], self.in_buffer.pop(0))
                else:
                    self.set(pidx[0], self.inputval)
                    # self.codes[self.codes[self.idx+1]] = self.inputval
                self.idx = self.idx+2
            elif opcode == 4:
                # if self.print:
                #     print('OUTPUT:')
                #     print(pvals[0])
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
                # self.idx = self.idx+1
                return -100000

def get_start_loc(map_str):
    for iy in range(1, len(map_str)):
        for ix in range(1, len(map_str[0])):
            if map_str[iy][ix] == '^':
                return (ix, iy)
    return None

def parse_turn(n):
    if n == 1:
        return 'L'
    else:
        return 'R'

def parse_scaffolding(map_str):
    rx, ry = get_start_loc(map_str)
    print('%d %d' % (rx, ry))

    start_pos = (rx, ry)
    avoid_pos = (-1, -1)
    lengths = []
    angle_prev = d_angle[(0,-1)]
    angle_change = []
    while start_pos != None:
        line_len, direction, start_pos, avoid_pos = parse_scaffolding_line(map_str, start_pos, avoid_pos)
        if start_pos != None:
            print(str(line_len) + ' ' + str(direction) + ' ' + str(start_pos) + ' ' + str(avoid_pos))
            lengths.append(line_len)
            angle_change.append((d_angle[direction] - angle_prev) % 4)
            angle_prev = d_angle[direction]

    turns = list(map(parse_turn, angle_change))

    print(lengths)
    print(turns)

    for i in range(len(lengths)):
        print(turns[i] + str(lengths[i]))

dirs = [(0,1), (0,-1), (-1,0), (1,0)]
d_angle = {(1,0):0, (0,-1):1, (-1,0):2, (0,1):3}

# start_pos, avoid_pos (don't go this way) ->
# line_len, direction, new_pos, prev_pos (don't go this way)
# position format: (x, y) <-> map_str[y][x]
def parse_scaffolding_line(map_str, start_pos, avoid_pos):
    ysize = len(map_str)
    xsize = len(map_str[0])
    next_dir = None
    for d in dirs:
        x2 = start_pos[0] + d[0]
        y2 = start_pos[1] + d[1]
        next_pos = (x2, y2)
        if next_pos != avoid_pos and x2 >= 0 and x2 < xsize and y2 >= 0 and y2 < ysize:
            if map_str[y2][x2] == '#':
                next_dir = d
    if next_dir == None:
        return None, None, None, None

    ptr = (start_pos[0] + next_dir[0], start_pos[1] + next_dir[1])
    line_len = 0
    while ptr[0] >= 0 and ptr[0] < xsize and ptr[1] >= 0 and ptr[1] < ysize and map_str[ptr[1]][ptr[0]] == '#':
        line_len += 1
        ptr = (ptr[0] + next_dir[0], ptr[1] + next_dir[1])
    end_pos = (ptr[0] - next_dir[0], ptr[1] - next_dir[1])
    avoid_pos = (end_pos[0] - next_dir[0], end_pos[1] - next_dir[1])

    return line_len, next_dir, end_pos, avoid_pos

if __name__ == '__main__':
    import copy
    codes = [1,330,331,332,109,4286,1102,1,1182,16,1101,1491,0,24,102,1,0,570,1006,570,36,1002,571,1,0,1001,570,-1,570,1001,24,1,24,1106,0,18,1008,571,0,571,1001,16,1,16,1008,16,1491,570,1006,570,14,21102,58,1,0,1105,1,786,1006,332,62,99,21101,0,333,1,21101,0,73,0,1105,1,579,1102,0,1,572,1102,1,0,573,3,574,101,1,573,573,1007,574,65,570,1005,570,151,107,67,574,570,1005,570,151,1001,574,-64,574,1002,574,-1,574,1001,572,1,572,1007,572,11,570,1006,570,165,101,1182,572,127,1002,574,1,0,3,574,101,1,573,573,1008,574,10,570,1005,570,189,1008,574,44,570,1006,570,158,1106,0,81,21101,0,340,1,1106,0,177,21101,0,477,1,1106,0,177,21102,514,1,1,21102,176,1,0,1106,0,579,99,21102,1,184,0,1105,1,579,4,574,104,10,99,1007,573,22,570,1006,570,165,101,0,572,1182,21101,0,375,1,21101,0,211,0,1106,0,579,21101,1182,11,1,21101,0,222,0,1105,1,979,21102,388,1,1,21102,233,1,0,1106,0,579,21101,1182,22,1,21102,244,1,0,1105,1,979,21101,0,401,1,21102,255,1,0,1105,1,579,21101,1182,33,1,21101,266,0,0,1106,0,979,21101,414,0,1,21102,277,1,0,1106,0,579,3,575,1008,575,89,570,1008,575,121,575,1,575,570,575,3,574,1008,574,10,570,1006,570,291,104,10,21101,0,1182,1,21101,313,0,0,1105,1,622,1005,575,327,1101,0,1,575,21102,1,327,0,1105,1,786,4,438,99,0,1,1,6,77,97,105,110,58,10,33,10,69,120,112,101,99,116,101,100,32,102,117,110,99,116,105,111,110,32,110,97,109,101,32,98,117,116,32,103,111,116,58,32,0,12,70,117,110,99,116,105,111,110,32,65,58,10,12,70,117,110,99,116,105,111,110,32,66,58,10,12,70,117,110,99,116,105,111,110,32,67,58,10,23,67,111,110,116,105,110,117,111,117,115,32,118,105,100,101,111,32,102,101,101,100,63,10,0,37,10,69,120,112,101,99,116,101,100,32,82,44,32,76,44,32,111,114,32,100,105,115,116,97,110,99,101,32,98,117,116,32,103,111,116,58,32,36,10,69,120,112,101,99,116,101,100,32,99,111,109,109,97,32,111,114,32,110,101,119,108,105,110,101,32,98,117,116,32,103,111,116,58,32,43,10,68,101,102,105,110,105,116,105,111,110,115,32,109,97,121,32,98,101,32,97,116,32,109,111,115,116,32,50,48,32,99,104,97,114,97,99,116,101,114,115,33,10,94,62,118,60,0,1,0,-1,-1,0,1,0,0,0,0,0,0,1,42,16,0,109,4,1202,-3,1,586,21001,0,0,-1,22101,1,-3,-3,21102,1,0,-2,2208,-2,-1,570,1005,570,617,2201,-3,-2,609,4,0,21201,-2,1,-2,1106,0,597,109,-4,2106,0,0,109,5,1202,-4,1,629,21002,0,1,-2,22101,1,-4,-4,21102,1,0,-3,2208,-3,-2,570,1005,570,781,2201,-4,-3,653,20101,0,0,-1,1208,-1,-4,570,1005,570,709,1208,-1,-5,570,1005,570,734,1207,-1,0,570,1005,570,759,1206,-1,774,1001,578,562,684,1,0,576,576,1001,578,566,692,1,0,577,577,21101,0,702,0,1106,0,786,21201,-1,-1,-1,1106,0,676,1001,578,1,578,1008,578,4,570,1006,570,724,1001,578,-4,578,21102,1,731,0,1106,0,786,1106,0,774,1001,578,-1,578,1008,578,-1,570,1006,570,749,1001,578,4,578,21102,1,756,0,1106,0,786,1106,0,774,21202,-1,-11,1,22101,1182,1,1,21102,1,774,0,1105,1,622,21201,-3,1,-3,1105,1,640,109,-5,2106,0,0,109,7,1005,575,802,21002,576,1,-6,20101,0,577,-5,1106,0,814,21102,0,1,-1,21102,1,0,-5,21101,0,0,-6,20208,-6,576,-2,208,-5,577,570,22002,570,-2,-2,21202,-5,43,-3,22201,-6,-3,-3,22101,1491,-3,-3,2101,0,-3,843,1005,0,863,21202,-2,42,-4,22101,46,-4,-4,1206,-2,924,21102,1,1,-1,1106,0,924,1205,-2,873,21102,1,35,-4,1105,1,924,1202,-3,1,878,1008,0,1,570,1006,570,916,1001,374,1,374,1202,-3,1,895,1102,2,1,0,1201,-3,0,902,1001,438,0,438,2202,-6,-5,570,1,570,374,570,1,570,438,438,1001,578,558,921,21001,0,0,-4,1006,575,959,204,-4,22101,1,-6,-6,1208,-6,43,570,1006,570,814,104,10,22101,1,-5,-5,1208,-5,65,570,1006,570,810,104,10,1206,-1,974,99,1206,-1,974,1101,0,1,575,21101,973,0,0,1106,0,786,99,109,-7,2105,1,0,109,6,21101,0,0,-4,21101,0,0,-3,203,-2,22101,1,-3,-3,21208,-2,82,-1,1205,-1,1030,21208,-2,76,-1,1205,-1,1037,21207,-2,48,-1,1205,-1,1124,22107,57,-2,-1,1205,-1,1124,21201,-2,-48,-2,1106,0,1041,21102,-4,1,-2,1105,1,1041,21101,-5,0,-2,21201,-4,1,-4,21207,-4,11,-1,1206,-1,1138,2201,-5,-4,1059,2102,1,-2,0,203,-2,22101,1,-3,-3,21207,-2,48,-1,1205,-1,1107,22107,57,-2,-1,1205,-1,1107,21201,-2,-48,-2,2201,-5,-4,1090,20102,10,0,-1,22201,-2,-1,-2,2201,-5,-4,1103,2101,0,-2,0,1105,1,1060,21208,-2,10,-1,1205,-1,1162,21208,-2,44,-1,1206,-1,1131,1106,0,989,21102,1,439,1,1106,0,1150,21102,1,477,1,1106,0,1150,21102,514,1,1,21101,0,1149,0,1105,1,579,99,21101,0,1157,0,1105,1,579,204,-2,104,10,99,21207,-3,22,-1,1206,-1,1138,1201,-5,0,1176,2102,1,-4,0,109,-6,2105,1,0,4,11,32,1,9,1,32,1,9,1,32,1,9,1,32,1,9,1,32,1,9,1,32,1,9,1,32,1,9,1,32,13,40,1,1,1,40,1,1,1,40,1,1,1,40,11,34,1,7,1,34,1,7,1,34,1,7,1,34,11,3,13,24,1,1,1,3,1,36,1,1,1,3,1,36,1,1,1,3,1,36,1,1,1,3,1,36,1,1,1,3,1,36,1,1,1,3,1,36,1,1,1,3,1,28,9,1,1,3,1,28,1,9,1,3,1,16,9,3,1,5,9,16,1,7,1,3,1,5,1,3,1,20,1,7,1,1,13,20,1,7,1,1,1,1,1,5,1,24,1,7,1,1,1,1,1,5,1,24,1,7,1,1,1,1,1,5,1,24,1,7,1,1,1,1,1,5,1,24,1,7,1,1,1,1,1,5,1,24,13,5,1,32,1,1,1,7,1,20,13,1,1,7,1,20,1,13,1,7,1,20,1,13,9,20,1,42,1,1,9,32,1,1,1,40,1,1,1,40,1,1,1,40,1,1,1,40,1,1,1,40,1,1,1,40,1,1,1,40,11,34,1,7,1,34,1,7,1,34,1,7,1,34,11,40,1,1,1,40,1,1,1,40,1,1,1,40,13,32,1,9,1,32,1,9,1,32,1,9,1,32,1,9,1,32,1,9,1,32,1,9,1,32,1,9,1,32,11,20]
    codes2 = copy.deepcopy(codes)
    ic = IntComp(copy.deepcopy(codes), 0) 

    out_str = ''
    while True:
        res = ic.run(0)
        if res == -100000:
            break
        out_str = out_str + chr(res)
    map_str = [list(row) for row in out_str.split('\n') if len(row) > 0]

    print(out_str)
    # for i in range(len(map_str)):
    #   print(str(i) + ': ' + str(map_str[i]))

    intersection_sum = 0
    for iy in range(1, len(map_str)-1):
        for ix in range(1, len(map_str[0])-1):
            if map_str[iy][ix] == '#' and map_str[iy][ix+1] == '#' and map_str[iy+1][ix] == '#' and map_str[iy][ix-1] == '#' and map_str[iy-1][ix] == '#':
                # print("%d, %d" % (ix, iy))
                intersection_sum += ix*iy
    print(intersection_sum)

    parse_scaffolding(map_str)

    ic2 = IntComp(copy.deepcopy(codes2), 65)

    ic2.codes[0] = 2
    print('code switch')

    ysize = len(map_str)
    xsize = len(map_str[0])
    for i in range((xsize+1)*ysize):
        res = ic2.run(0)
        if res >= 0 and res < 128:
            print(chr(res), end = "")


    # print(ic2.print)
    in_strs = ['A,B,A,B,C,C,B,A,B,C\n', 'L,12,L,10,R,8,L,12\n', 'R,8,R,10,R,12\n', 'L,10,R,12,R,8\n', 'n\n']
    in_bufs = [[ord(c) for c in list(in_str)] for in_str in in_strs]
    # print(ascii_codes)

    while True:
        res = ic2.run(0)
        if res >= 0 and res < 128:
            print(chr(res), end = "")
        if chr(res) == ':':
            break

    ic2.use_in_buffer = True

    res = ic2.run(0)
    ic2.in_buffer = in_bufs[0]

    count = 0
    while True:
        count += 1
        res = ic2.run(0)
        # print('output %d' % res)
        if res >= 0 and res < 128:
            print(chr(res), end = "")
        else:
            print('output %d' % res)
        if chr(res) == ':':
            break        
        if res == -100000:
            break

    res = ic2.run(0)
    ic2.in_buffer = in_bufs[1]
    while True:
        count += 1
        res = ic2.run(0)
        # print('output %d' % res)
        if res >= 0 and res < 128:
            print(chr(res), end = "")
        else:
            print('output %d' % res)
        if chr(res) == ':':
            break        
        if res == -100000:
            break

    res = ic2.run(0)
    ic2.in_buffer = in_bufs[2]
    while True:
        count += 1
        res = ic2.run(0)
        # print('output %d' % res)
        if res >= 0 and res < 128:
            print(chr(res), end = "")
        else:
            print('output %d' % res)
        if chr(res) == ':':
            break        
        if res == -100000:
            break

    res = ic2.run(0)
    ic2.in_buffer = in_bufs[3]
    while True:
        count += 1
        res = ic2.run(0)
        # print('output %d' % res)
        if res >= 0 and res < 128:
            print(chr(res), end = "")
        else:
            print('output %d' % res)
        if chr(res) == '?':
            break        
        if res == -100000:
            break

    res = ic2.run(0)
    ic2.in_buffer = in_bufs[4]
    while True:
        count += 1
        res = ic2.run(0)
        # print('output %d' % res)
        if res >= 0 and res < 128:
            print(chr(res), end = "")
        else:
            print('output %d' % res)
        # if chr(res) == ':':
        #     break        
        if res == -100000:
            break

    print('count %d' % count)