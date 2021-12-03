import numpy as np

file1 = open('day_3_input.txt', 'r')
lines = file1.read().splitlines()
# lines = """00100
# 11110
# 10110
# 10111
# 10101
# 01111
# 00111
# 11100
# 10000
# 11001
# 00010
# 01010""".splitlines()

s_len = len(lines[0])

count0 = np.zeros(s_len)
for l in lines:
    for k in range(s_len):
        if l[k] == '0':
            count0[k] += 1
n_lines = len(lines)
mcb = count0 > (n_lines/2)
lcb = count0 < (n_lines/2)
print(mcb)
powers = np.power(2, np.flip(np.array(list(range(s_len)))))
mcb_int = np.dot(mcb, powers)
lcb_int = np.dot(lcb, powers)
print(mcb_int * lcb_int)


def oxy_rating(idx, strs):
    n_str = len(strs)
    count1 = 0
    for l in strs:
        if l[idx] == '1':
            count1 += 1
    if count1 >= n_str/2:
        return '1'
    else:
        return '0'


def CO2_rating(idx, strs):
    n_str = len(strs)
    count0 = 0
    for l in strs:
        if l[idx] == '0':
            count0 += 1
    if count0 <= n_str/2:
        return '0'
    else:
        return '1'


def filter_rating(strs, fn):
    idx = 0
    my_strs = strs.copy()
    while len(my_strs) > 1:
        bit_select = fn(idx, my_strs)
        my_strs = [num for num in my_strs if num[idx] == bit_select]
        idx += 1
    return int(my_strs[0], 2)


print(filter_rating(lines, CO2_rating)*filter_rating(lines, oxy_rating))
