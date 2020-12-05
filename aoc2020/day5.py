import numpy as np

file1 = open('day_5_input.txt', 'r')
lines = file1.read().splitlines()


def char_val(c):
    if c == 'F':
        return 0
    elif c == 'B':
        return 1
    elif c == 'R':
        return 1
    elif c == 'L':
        return 0
    print('oh no')
    return 0


def get_id(s):
    bin_digits = np.array([char_val(c) for c in s])
    # print(bin_digits)
    return np.dot(2 ** np.flip(np.arange(len(s))), bin_digits)


ids = set()

max_id = -1
for l in lines:
    m_id = get_id(l)
    ids.add(m_id)
    if m_id > max_id:
        max_id = m_id

print(max_id)

for a in range(max_id + 1):
    if a not in ids and (a-1) in ids and (a+1) in ids:
        print(a)