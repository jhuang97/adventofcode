from collections import deque
import re

file1 = open('day_14_input.txt', 'r')
lines = file1.read().splitlines()


def apply_mask(mask, val):
    vstr = "{0:36b}".format(val).replace(' ', '0')
    res_str = ""
    for i in range(36):
        if mask[i] == 'X':
            res_str += vstr[i]
        else:
            res_str += mask[i]
    return int(res_str, 2)


def apply_mask2(mask, addr):
    vstr = "{0:36b}".format(addr).replace(' ', '0')
    res_str = ""
    for i in range(36):
        if mask[i] == 'X':
            res_str += 'X'
        elif mask[i] == '1':
            res_str += '1'
        elif mask[i] == '0':
            res_str += vstr[i]
    addrs = []
    floating_strs = deque([res_str])
    while floating_strs:
        next = floating_strs.pop()
        if 'X' not in next:
            addrs.append(next)
        else:
            idx = next.index('X')
            nlist = list(next)
            nlist[idx] = '0'
            floating_strs.append("".join(nlist))
            nlist[idx] = '1'
            floating_strs.append("".join(nlist))
    return addrs



mask = ''
mem = {}
for l in lines:
    if l.startswith('mask'):
        m = re.match(r'mask = ([01X]+)', l)
        mask = m.group(1)
        # print(mask.count('X'))
    elif l.startswith('mem'):
        m = re.match(r'mem\[(\d+)\] = (\d+)', l)
        addr = int(m.group(1))
        val = int(m.group(2))
        mem[addr] = apply_mask(mask, val)

total = 0
for k, v in mem.items():
    total += v
print(total)


mask = ''
mem = {}
for l in lines:
    if l.startswith('mask'):
        m = re.match(r'mask = ([01X]+)', l)
        mask = m.group(1)
    elif l.startswith('mem'):
        m = re.match(r'mem\[(\d+)\] = (\d+)', l)
        addr = int(m.group(1))
        val = int(m.group(2))
        addrs = apply_mask2(mask, addr)
        for a in addrs:
            mem[int(a, 2)] = val

total = 0
for k, v in mem.items():
    total += v
print(total)