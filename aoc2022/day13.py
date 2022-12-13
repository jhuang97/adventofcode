from functools import total_ordering

file1 = open('day13_in.txt', 'r')
# file1 = open('day13_test.txt', 'r')
parts = file1.read().strip().split('\n\n')


@total_ordering
class Packet:
    def __init__(self, s):
        self.s = s

    def __eq__(self, other):
        return right_order(eval(self.s), eval(other.s)) is None

    def __lt__(self, other):
        return right_order(eval(self.s), eval(other.s))


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
    packets = [eval(l) for l in lines]
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