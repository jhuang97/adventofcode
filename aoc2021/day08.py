import itertools

file1 = open('day_8_input.txt', 'r')
lines = file1.read().strip().split('\n')

outputs = [l.split(' | ')[1] for l in lines]

# digit_to_signal = {}
# num_seg = [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]
# num_seg_to_digit = {2:1, 4:4, 3:7, 7:8}

def count_digits(l) :
    count = 0
    signals = l.split(' ')
    for s in signals:
        # 1 - 2, 4 - 4, 7 - 3, 8 - 7
        if len(s) in [2, 3, 4, 7]:
            count += 1
            # digit_to_signal[num_seg_to_digit[len(s)]] = s
    return count

count = 0
for l in outputs:
    count += count_digits(l)
print(count)
# print(digit_to_signal)


digit_to_seg0 = ['abcefg', 'cf', 'acdeg', 'acdfg', 'bcdf', 'abdfg', 'abdefg', 'acf', 'abcdefg', 'abcdfg']
str_to_digit = {}
for k in range(10):
    str_to_digit[digit_to_seg0[k]] = k


def alphabetize(s):
    return ''.join(sorted(list(s)))


def is_consistent(mapping, strs):
    for s in strs:
        new_str = ''.join(sorted([mapping[c] for c in s]))
        if new_str not in digit_to_seg0:
            return False
    return True


def apply_mapping(mapping, outputs, str_to_digit):
    s = ''
    for output in outputs:
        new_str = ''.join(sorted([mapping[c] for c in output]))
        s += str(str_to_digit[new_str])
    return int(s)


def decode(l):
    puts = l.split(' | ')
    inputs = puts[0].split()
    outputs = puts[1].split()
    all_puts = inputs + outputs

    # first get strings of length 2, 3, 4, 7
    # mapping = {}
    # for test_len in [2, 3, 4, 5, 6]:
    #     for s in all_puts:
    #         if len(s) == test_len:
    #             print(alphabetize(s))

    for p in itertools.permutations(list('abcdefg')):
        mapping = dict(zip(list('abcdefg'), p))
        if is_consistent(mapping, all_puts):
            # print(mapping)
            break
    num = apply_mapping(mapping, outputs, str_to_digit)
    return num

    # uniq_str = {}
    # for s in all_puts:
    #     if len(s) in [2, 3, 4]:
    #         uniq_str[len(s)] = set(s)
    # (mapping['a'],) = uniq_str[3].difference(uniq_str[2])

    # for s in all_puts:
    #     for seg0 in digit_to_seg0:
    #         if len(s) == len(seg0):
    #             mapping[alphabetize(s)] = set(seg0)

    # known_keys = mapping.keys()
    # diffs = []
    # print(mapping)
    # for s1 in known_keys:
    #     for s2 in known_keys:
    #         if len(s1) < len(s2):
    #             ss1 = set(s1)
    #             ss2 = set(s2)
    #             if ss1.issubset(ss2) and mapping[s1].issubset(mapping[s2]):
    #                 str_diff = alphabetize(ss2.difference(ss1))
    #                 if str_diff not in known_keys:
    #                     print(s1, s2, mapping[s1], mapping[s2])
    #                     diffs.append((s1, s2, str_diff))
    # for s1, s2, str_diff in diffs:
    #     mapping[str_diff] = mapping[s2].difference(s1)
    #     print(str_diff, mapping[s2].difference(s1))

    # print(be_possible)

total = 0
for l in lines:
    total += decode(l)

print(total)
