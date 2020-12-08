import copy

file1 = open('day_8_input.txt', 'r')
lines = file1.read().splitlines()


def read_line(line):
    t = line.split(' ')
    return [t[0], int(t[1])]


def execute(cmd):
    visited = []
    ptr = 0
    acc = 0
    while True:
        visited.append(ptr)
        if cmd[ptr][0] == 'nop':
            ptr += 1
        elif cmd[ptr][0] == 'jmp':
            ptr += cmd[ptr][1]
        elif cmd[ptr][0] == 'acc':
            acc += cmd[ptr][1]
            ptr += 1

        if ptr in visited:
            return True, acc

        if ptr >= len(cmd):
            return False, acc


cmd = [read_line(l) for l in lines]
print(execute(cmd))

for i in range(len(cmd)):
    cmd2 = copy.deepcopy(cmd)
    if cmd[i][0] == 'nop':
        cmd2[i][0] = 'jmp'
    elif cmd[i][0] == 'jmp':
        cmd2[i][0] = 'nop'
    else:
        continue

    (inf_loop, acc) = execute(cmd2)
    if not inf_loop:
        print(acc)
