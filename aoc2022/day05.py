file1 = open('day05_in.txt', 'r')
parts = file1.read().split('\n\n')

stack_l = parts[0].split('\n')
indices = [0]
for k in range(1, 10):
    indices.append(stack_l[-1].index(str(k)))

stacks = stack_l[:-1]
stacks.reverse()

moves_str = parts[1].strip().split('\n')
n_move, i1s, i2s = [], [], []
for l in moves_str:
    s = l.split()
    n_move.append(int(s[1]))
    i1s.append(int(s[3]))
    i2s.append(int(s[5]))

for reverse in [True, False]:
    stack_str = ['']
    for k in range(1, 10):
        my_str = ''
        for l in stacks:
            my_str += l[indices[k]]
        stack_str.append(my_str.strip())
    # top of stack = end of string

    for n, i1, i2 in zip(n_move, i1s, i2s):
        stack_str[i1], tmp = stack_str[i1][:-n], stack_str[i1][-n:]
        if reverse:
            stack_str[i2] = stack_str[i2] + tmp[::-1]
        else:
            stack_str[i2] = stack_str[i2] + tmp

    out_str = ''
    for s in stack_str[1:]:
        out_str += s[-1]
    print(out_str)