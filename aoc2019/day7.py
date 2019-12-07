class Amplifier:
    def __init__(self, codes, phase, inputval):
        self.codes = codes
        self.phase = phase
        self.inputval = inputval
        self.first_input = True
        self.idx = 0

    def run(self, iv2):
        self.inputval = iv2
        while True:
            mcode = self.codes[self.idx]
            opcode = mcode % 100
            pmodes = [mcode//100%10, mcode//1000%10, mcode//10000%10]
            pvals = [None, None, None]
            if opcode == 1 or opcode == 2 or opcode == 7 or opcode == 8:
                for i in range(3):
                    if pmodes[i] == 0: # position
                        pvals[i] = self.codes[self.codes[self.idx+i+1]]
                    elif pmodes[i] == 1: # immediate
                        pvals[i] = self.codes[self.idx+i+1]
            elif opcode == 3 or opcode == 4:
                if pmodes[0] == 0:
                    pvals[0] = self.codes[self.codes[self.idx+1]]
                elif pmodes[0] == 1:
                    pvals[0] = self.codes[self.idx+1]
            elif opcode >= 5 and opcode <= 6:
                for i in range(2):
                    if pmodes[i] == 0: # position
                        pvals[i] = self.codes[self.codes[self.idx+i+1]]
                    elif pmodes[i] == 1: # immediate
                        pvals[i] = self.codes[self.idx+i+1]


            if opcode == 1:
                self.codes[self.codes[self.idx+3]] = pvals[0] + pvals[1]
                self.idx = self.idx + 4
            elif opcode == 2:
                self.codes[self.codes[self.idx+3]] = pvals[0] * pvals[1]
                self.idx = self.idx + 4
            elif opcode == 3:
                if self.first_input:
                    self.codes[self.codes[self.idx+1]] = self.phase
                    self.first_input = False
                else:
                    self.codes[self.codes[self.idx+1]] = self.inputval
                self.idx = self.idx+2
            elif opcode == 4:
                print('OUTPUT:')
                print(pvals[0])
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
                    self.codes[self.codes[self.idx+3]] = 1
                else:
                    self.codes[self.codes[self.idx+3]] = 0
                self.idx = self.idx+4
            elif opcode == 8:
                if pvals[0] == pvals[1]:
                    self.codes[self.codes[self.idx+3]] = 1
                else:
                    self.codes[self.codes[self.idx+3]] = 0
                self.idx = self.idx+4
            elif opcode == 99:
                return -100000

def intcode_computer(codes, phase, inputval):
    idx = 0
    first_input = True
    
    while True:
        mcode = codes[idx]
        opcode = mcode % 100
        pmodes = [mcode//100%10, mcode//1000%10, mcode//10000%10]
        pvals = [None, None, None]
        if opcode == 1 or opcode == 2 or opcode == 7 or opcode == 8:
            for i in range(3):
                if pmodes[i] == 0: # position
                    pvals[i] = codes[codes[idx+i+1]]
                elif pmodes[i] == 1: # immediate
                    pvals[i] = codes[idx+i+1]
        elif opcode == 3 or opcode == 4:
            if pmodes[0] == 0:
                pvals[0] = codes[codes[idx+1]]
            elif pmodes[0] == 1:
                pvals[0] = codes[idx+1]
        elif opcode >= 5 and opcode <= 6:
            for i in range(2):
                if pmodes[i] == 0: # position
                    pvals[i] = codes[codes[idx+i+1]]
                elif pmodes[i] == 1: # immediate
                    pvals[i] = codes[idx+i+1]


        if opcode == 1:
            codes[codes[idx+3]] = pvals[0] + pvals[1]
            idx = idx + 4
        elif opcode == 2:
            codes[codes[idx+3]] = pvals[0] * pvals[1]
            idx = idx + 4
        elif opcode == 3:
            if first_input:
                codes[codes[idx+1]] = phase
                first_input = False
            else:
                codes[codes[idx+1]] = inputval
            idx = idx+2
        elif opcode == 4:
            print('OUTPUT:')
            print(pvals[0])
            return pvals[0]
            idx=idx+2
        elif opcode == 5:
            if pvals[0] != 0:
                idx = pvals[1]
            else:
                idx = idx+3
        elif opcode == 6:
            if pvals[0] == 0:
                idx = pvals[1]
            else:
                idx = idx+3
        elif opcode == 7:
            if pvals[0] < pvals[1]:
                codes[codes[idx+3]] = 1
            else:
                codes[codes[idx+3]] = 0
            idx = idx+4
        elif opcode == 8:
            if pvals[0] == pvals[1]:
                codes[codes[idx+3]] = 1
            else:
                codes[codes[idx+3]] = 0
            idx = idx+4
        elif opcode == 99:
            return -100000

def new_thruster_program2(perm, codes):
    amps = [Amplifier(copy.deepcopy(codes), perm[i], 0) for i in range(5)]

    res = 0
    last_res = -1
    round_idx = 0
    while True:
        for idx in range(5):
            if round_idx == 0 and idx == 0:
                res = amps[idx].run(0)
            else:
                res = amps[idx].run(res)
            if res == -100000:
                if idx == 4:
                    return res
                return last_res

        round_idx = round_idx+1
        last_res = res

if __name__ == '__main__':
   
    # codes = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    # codes = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
    codes = [3,8,1001,8,10,8,105,1,0,0,21,46,67,76,97,118,199,280,361,442,99999,3,9,1002,9,3,9,101,4,9,9,102,3,9,9,1001,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,101,5,9,9,1002,9,2,9,101,2,9,9,4,9,99,3,9,101,4,9,9,4,9,99,3,9,1001,9,4,9,102,2,9,9,1001,9,4,9,1002,9,5,9,4,9,99,3,9,102,3,9,9,1001,9,2,9,1002,9,3,9,1001,9,3,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,99]

    import copy
    max_so_far = 0
    max_str = 0

    import itertools

    # for perm in list(itertools.permutations([0,1,2,3,4])):
    #     res = 0
    #     for idx in range(5):
    #         res = intcode_computer(copy.deepcopy(codes), perm[idx], res)
    #         if res > max_so_far:
    #             max_str = perm
    #             max_so_far = res

    for perm in list(itertools.permutations([5,6,7,8,9])):
        out = new_thruster_program2(perm, copy.deepcopy(codes))
        if out > max_so_far:
            max_str = perm[4] + 10*perm[3] + 100*perm[2] + 1000*perm[1] + 10000*perm[0]
            max_so_far = out

    print(max_str)
    print(max_so_far)
    