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

def print_map(screen):
    x1 = 10000
    x2 = -10000
    y1 = 10000
    y2 = -10000
    for coords in screen.keys():
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
    out_arr = [['_' for j in range(x2-x1+1)] for i in range(y2-y1+1)]
    obj_chars = ['.', '#']
    for coords, val in screen.items():
        out_arr[coords[1]-y1][coords[0]-x1] = obj_chars[val]

    for row in out_arr:
        print("".join(row))

def check_beam(codes, x, y):
    ic = IntComp(copy.deepcopy(codes), 0)
    ic.use_in_buffer = True
    ic.in_buffer = [x, y]
    return ic.run(0)

def fit_square(codes, x0, y0, side_len):
    if check_beam(codes, x0, y0) != 1:
        print('bad start')
        return None

    x = x0
    y = y0
    go_right = True
    while True:
        check_here = False
        if go_right:
            x += 1
        else:
            y += 1
        if check_beam(codes, x, y) == 1:
            go_right = True
            if x - side_len + 1 >= 0:
                check_here = True
        else:
            go_right = False

        if check_here:
            if check_beam(codes, x-side_len+1, y+side_len-1) == 1:
                break

    return x-side_len+1, y


if __name__ == '__main__':
    import copy
    codes = [109,424,203,1,21101,11,0,0,1106,0,282,21101,18,0,0,1106,0,259,1202,1,1,221,203,1,21102,31,1,0,1105,1,282,21101,0,38,0,1106,0,259,21002,23,1,2,22102,1,1,3,21102,1,1,1,21102,57,1,0,1106,0,303,2102,1,1,222,21002,221,1,3,20102,1,221,2,21102,1,259,1,21102,1,80,0,1105,1,225,21102,105,1,2,21102,91,1,0,1105,1,303,1202,1,1,223,20102,1,222,4,21102,259,1,3,21101,225,0,2,21101,225,0,1,21102,118,1,0,1106,0,225,20101,0,222,3,21101,157,0,2,21102,133,1,0,1106,0,303,21202,1,-1,1,22001,223,1,1,21102,1,148,0,1105,1,259,2101,0,1,223,20101,0,221,4,20101,0,222,3,21102,21,1,2,1001,132,-2,224,1002,224,2,224,1001,224,3,224,1002,132,-1,132,1,224,132,224,21001,224,1,1,21102,195,1,0,105,1,108,20207,1,223,2,20101,0,23,1,21102,-1,1,3,21101,0,214,0,1106,0,303,22101,1,1,1,204,1,99,0,0,0,0,109,5,1201,-4,0,249,21202,-3,1,1,21202,-2,1,2,22102,1,-1,3,21101,0,250,0,1106,0,225,22101,0,1,-4,109,-5,2106,0,0,109,3,22107,0,-2,-1,21202,-1,2,-1,21201,-1,-1,-1,22202,-1,-2,-2,109,-3,2105,1,0,109,3,21207,-2,0,-1,1206,-1,294,104,0,99,22102,1,-2,-2,109,-3,2106,0,0,109,5,22207,-3,-4,-1,1206,-1,346,22201,-4,-3,-4,21202,-3,-1,-1,22201,-4,-1,2,21202,2,-1,-1,22201,-4,-1,1,21201,-2,0,3,21101,0,343,0,1105,1,303,1105,1,415,22207,-2,-3,-1,1206,-1,387,22201,-3,-2,-3,21202,-2,-1,-1,22201,-3,-1,3,21202,3,-1,-1,22201,-3,-1,2,21201,-4,0,1,21102,384,1,0,1106,0,303,1106,0,415,21202,-4,-1,-4,22201,-4,-3,-4,22202,-3,-2,-2,22202,-2,-4,-4,22202,-3,-2,-3,21202,-4,-1,-2,22201,-3,-2,1,21201,1,0,-4,109,-5,2105,1,0]

    # part 1
    # count = 0
    # t_map = {}
    # for x in range(50):
    #     for y in range(50):
    #         res = check_beam(codes, x, y)
    #         t_map[(x,y)] = res
    #         if res == 1:
    #             count += 1

    # print_map(t_map)
    # print(count)

    # part 2
    xi, yi = fit_square(codes, 5, 4, 100)
    print(10000*xi + yi)