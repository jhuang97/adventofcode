file1 = open('day11_in.txt', 'r')
# file1 = open('day11_test.txt', 'r')
m_str = file1.read().strip().split('\n\n')
m = []


def expect_s(s, expect):
    if not s.startswith(expect):
        print('oh no', s, expect)
    return s[len(expect):]


class Monkey:
    def __init__(self, input_str):
        lines = input_str.splitlines()
        self.items = [int(n) for n in expect_s(lines[1].strip(), 'Starting items: ').split(', ')]
        op_parts = expect_s(lines[2].strip(), 'Operation: new = old ').split()
        if op_parts[0] == '+':
            self.op = lambda n: n + int(op_parts[1])
        elif op_parts[0] == '*':
            if op_parts[1] == 'old':
                self.op = lambda n: n*n
            else:
                self.op = lambda n: n * int(op_parts[1])
        else:
            print('oh no')
        self.div_fac = int(expect_s(lines[3].strip(), 'Test: divisible by '))
        self.true_dest = int(expect_s(lines[4].strip(), 'If true: throw to monkey '))
        self.false_dest = int(expect_s(lines[5].strip(), 'If false: throw to monkey '))


m = [Monkey(ms) for ms in m_str]

n_inspect = [0] * len(m)
for _ in range(20):
    for im, monkey in enumerate(m):
        curr_list = monkey.items
        for item in curr_list:
            w = monkey.op(item)
            w = w//3
            dest = monkey.true_dest if w % monkey.div_fac == 0 else monkey.false_dest
            # print(im, item, w, dest)
            m[dest].items.append(w)
        n_inspect[im] += len(curr_list)
        monkey.items = []

# for im, monkey in enumerate(m):
#     print(im, monkey.items, monkey.op(1), n_inspect[im])

sort_n = sorted(n_inspect)
print(sort_n[-1]*sort_n[-2])


m = [Monkey(ms) for ms in m_str]
mod_prod = 1
for monkey in m:
    mod_prod *= monkey.div_fac

n_inspect = [0] * len(m)
for _ in range(10000):
    for im, monkey in enumerate(m):
        curr_list = monkey.items
        for item in curr_list:
            w = monkey.op(item)
            w %= mod_prod
            dest = monkey.true_dest if w % monkey.div_fac == 0 else monkey.false_dest
            # print(im, item, w, dest)
            m[dest].items.append(w)
        n_inspect[im] += len(curr_list)
        monkey.items = []

# for im, monkey in enumerate(m):
#     print(im, monkey.items, monkey.op(1), n_inspect[im])

sort_n = sorted(n_inspect)
print(sort_n[-1]*sort_n[-2])