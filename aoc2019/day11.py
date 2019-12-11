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

class HullRobot:
    def __init__(self):
        self.map = {}
        self.pos = (0,0)
        self.dirs = [(0,1), (-1, 0), (0, -1), (1,0)]
        self.didx = 0

    def turn(self, tval):
        if tval == 0:
            self.didx = (self.didx + 1) % 4
        elif tval == 1:
            self.didx = (self.didx - 1) % 4

    def step(self):
        self.pos = (self.pos[0] + self.dirs[self.didx][0], self.pos[1] + self.dirs[self.didx][1])

    def paint(self, pval):
        self.map[self.pos] = pval

    def get_color(self):
        if self.pos in self.map:
            return self.map[self.pos]
        else:
            return 0 # black


if __name__ == '__main__':
   
    import copy

    codes = [3,8,1005,8,324,1106,0,11,0,0,0,104,1,104,0,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,1001,8,0,29,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,101,0,8,50,1,1106,9,10,1,102,15,10,2,1003,3,10,1,3,19,10,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,0,10,4,10,1001,8,0,89,1,1105,9,10,2,1103,1,10,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,1,10,4,10,1001,8,0,119,1006,0,26,1,109,7,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,1,8,10,4,10,1002,8,1,147,1006,0,75,1,1005,17,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,102,1,8,176,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,102,1,8,199,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,102,1,8,220,2,103,10,10,1,1,0,10,1,102,17,10,3,8,1002,8,-1,10,101,1,10,10,4,10,108,1,8,10,4,10,101,0,8,254,2,1001,10,10,1006,0,12,1,3,6,10,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,0,10,4,10,102,1,8,288,2,1106,9,10,2,1009,6,10,2,1101,18,10,2,103,8,10,101,1,9,9,1007,9,1045,10,1005,10,15,99,109,646,104,0,104,1,21101,838211318676,0,1,21102,341,1,0,1106,0,445,21101,0,838211051932,1,21101,0,352,0,1106,0,445,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21101,0,21704576195,1,21101,0,399,0,1106,0,445,21101,0,179356830951,1,21101,410,0,0,1105,1,445,3,10,104,0,104,0,3,10,104,0,104,0,21102,837897052948,1,1,21102,1,433,0,1106,0,445,21102,709052085092,1,1,21102,1,444,0,1105,1,445,99,109,2,21201,-1,0,1,21101,0,40,2,21102,476,1,3,21102,466,1,0,1105,1,509,109,-2,2105,1,0,0,1,0,0,1,109,2,3,10,204,-1,1001,471,472,487,4,0,1001,471,1,471,108,4,471,10,1006,10,503,1102,1,0,471,109,-2,2106,0,0,0,109,4,2102,1,-1,508,1207,-3,0,10,1006,10,526,21101,0,0,-3,21201,-3,0,1,21201,-2,0,2,21101,0,1,3,21101,545,0,0,1105,1,550,109,-4,2105,1,0,109,5,1207,-3,1,10,1006,10,573,2207,-4,-2,10,1006,10,573,21201,-4,0,-4,1105,1,641,22102,1,-4,1,21201,-3,-1,2,21202,-2,2,3,21101,592,0,0,1105,1,550,21201,1,0,-4,21102,1,1,-1,2207,-4,-2,10,1006,10,611,21101,0,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,633,21202,-1,1,1,21101,633,0,0,106,0,508,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2105,1,0]

    # part 1
    ic = IntComp(copy.deepcopy(codes), 0)
    hr = HullRobot()
    res = 0
    while True:
        res = ic.run(hr.get_color())
        if res == -100000:
            break
        hr.paint(res)
        res = ic.run(hr.get_color())
        if res == -100000:
            break
        hr.turn(res)
        hr.step()

    print("num panels %d" % len(hr.map))

    # part 2
    ic = IntComp(copy.deepcopy(codes), 0)
    hr = HullRobot()
    hr.map[(0,0)] = 1
    res = 0
    while True:
        res = ic.run(hr.get_color())
        if res == -100000:
            break
        hr.paint(res)
        res = ic.run(hr.get_color())
        if res == -100000:
            break
        hr.turn(res)
        hr.step()

    for coord, color in hr.map.items():
        if color == 1:
            print("%d,%d" % coord)

    # I plotted this in Mathematica with ListPlot