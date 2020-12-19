file1 = open('day_19_input.txt', 'r')
sections = file1.read().split('\n\n')
rule_strs = sections[0].split('\n')
rules = dict()
for l in rule_strs:
    tokens = l.split(': ')
    if tokens[1] == '"a"':
        a_key = int(tokens[0])
    elif tokens[1] == '"b"':
        b_key = int(tokens[0])
    else:
        tokens2 = tokens[1].split()
        list_of_lists = []
        curr_list = []
        for t in tokens2:
            if t.isdigit():
                curr_list.append(int(t))
            else:
                list_of_lists.append(curr_list.copy())
                curr_list = []
        if curr_list:
            list_of_lists.append(curr_list.copy())
        rules[int(tokens[0])] = list_of_lists
        # print(tokens2)
        # print(list_of_lists)

msgs = sections[1].splitlines()


def m(memo, key, val):
    memo[key] = val
    return val


def get_pat_len(idx, rules, memo):
    if idx in memo:
        return memo[idx]
    if idx == a_key or idx == b_key:
        return m(memo, idx, 1)

    prev_total = -1
    for i, r in enumerate(rules[idx]):
        total = 0
        for sub_key in r:
            total += get_pat_len(sub_key, rules, memo)
        m(memo, idx, total)
        if i > 0:
            if total != prev_total:
                print('oh no')
        prev_total = total
    return prev_total


len_memo = dict()
get_pat_len(0, rules, len_memo)


def match(s, idx):
    if len(s) != len_memo[idx]:
        return False
    if idx == a_key:
        return s == 'a'
    if idx == b_key:
        return s == 'b'
    for r in rules[idx]:
        ptr = 0
        matches_rule = True
        for sub_key in r:
            if not match(s[ptr:ptr+len_memo[sub_key]], sub_key):
                matches_rule = False
            ptr += len_memo[sub_key]
        if matches_rule:
            return True
    return False


print(sum([1 for l in msgs if match(l, 0)]))

len_memo2 = dict()
len_memo2[8] = float("nan")
len_memo2[11] = float("nan")
get_pat_len(42, rules, len_memo2)
get_pat_len(31, rules, len_memo2)

assert len_memo2[42] == len_memo2[31]
unit_len = len_memo2[42]


def match0(s):
    if len(s) < 3 * unit_len or len(s) % unit_len != 0:
        return False
    num_units = len(s) // unit_len
    count42 = 0
    count31 = 0
    switched = False
    for i in range(num_units):
        sub_str = s[unit_len*i:unit_len*(i+1)]
        if not switched:
            if match(sub_str, 42):
                count42 += 1
            elif match(sub_str, 31):
                switched = True
                count31 += 1
            else:
                return False
        else:
            if match(sub_str, 31):
                count31 += 1
            else:
                return False
    return count42 > count31 > 0


print(sum([1 for l in msgs if match0(l)]))
