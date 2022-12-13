from functools import total_ordering

file1 = open('day13_in.txt', 'r')
# file1 = open('day13_test.txt', 'r')
parts = file1.read().strip().split('\n\n')


def parse(s):
    if s.isnumeric():
        return int(s)
    elif s == '[]':
        return []
    elif s[0] == '[' and s[-1] == ']':
        level = 0
        s_idx = [1]
        e_idx = []
        for k in range(1, len(s)-1):
            if s[k] == '[':
                level += 1
            elif s[k] == ']':
                level -= 1
            elif s[k] == ',' and level == 0:
                e_idx.append(k)
                s_idx.append(k+1)
        e_idx.append(len(s)-1)
        return [parse(s[si:ei]) for si, ei in zip(s_idx, e_idx)]
    print('oh no', s)


@total_ordering
class Packet:
    def __init__(self, s):
        self.s = s

    def __eq__(self, other):
        return right_order(parse(self.s), parse(other.s)) is None

    def __lt__(self, other):
        return right_order(parse(self.s), parse(other.s))


def compare3(a, b):
    if a < b:
        return True
    elif a == b:
        return None
    elif a > b:
        return False


def right_order(a, b):
    # print('compare', a, b)
    if isinstance(a, int) and isinstance(b, int):
        return compare3(a, b)
    elif isinstance(a, list) and isinstance(b, list):
        la, lb = len(a), len(b)
        min_l = min(la, lb)
        if min_l == 0:
            return compare3(la, lb)
        else:
            for k in range(min_l):
                sub_compare = right_order(a[k], b[k])
                if sub_compare is not None:
                    return sub_compare
            return compare3(la, lb)
    elif isinstance(a, list) and isinstance(b, int):
        return right_order(a, [b])
    elif isinstance(a, int) and isinstance(b, list):
        return right_order([a], b)
    print('oh no')


total = 0
for pidx, part in enumerate(parts):
    lines = part.splitlines()
    packets = [parse(l) for l in lines]
    # print(pidx+1, right_order(packets[0], packets[1]))
    if right_order(packets[0], packets[1]):
        total += pidx+1
print(total)

all_p = [Packet('[[2]]'), Packet('[[6]]')]
for part in parts:
    lines = part.splitlines()
    all_p.append(Packet(lines[0]))
    all_p.append(Packet(lines[1]))
all_p.sort()

dividers = []
for idx, p in enumerate(all_p):
    # print(p.s)
    if p.s in ['[[2]]', '[[6]]']:
        dividers.append(idx+1)
# print(dividers)
print(dividers[0]*dividers[1])