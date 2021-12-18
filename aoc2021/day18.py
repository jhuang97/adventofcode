from math import ceil

file1 = open('day_18_input.txt', 'r')
lines = file1.read().strip().splitlines()


def to_list(s):
    l = list(s.replace(",", ""))
    for k in range(len(l)):
        if l[k] not in ['[', ']']:
            l[k] = int(l[k])
    return l


def try_explode(sn_list):
    level = 0
    explode_idx = -1
    for k in range(len(sn_list)-1):
        if sn_list[k] == '[':
            level += 1
        elif sn_list[k] == ']':
            level -= 1
        elif level >= 5 and isinstance(sn_list[k], int) and isinstance(sn_list[k+1], int):
            explode_idx = k
            break

    if explode_idx == -1:
        return sn_list, False
    else:
        # add left
        m = explode_idx-1
        while m >= 0:
            if isinstance(sn_list[m], int):
                sn_list[m] += sn_list[explode_idx]
                break
            m -= 1
        # add right
        m = explode_idx+2
        while m < len(sn_list):
            if isinstance(sn_list[m], int):
                sn_list[m] += sn_list[explode_idx+1]
                break
            m += 1
        sn_list[explode_idx-1:explode_idx+3] = [0]
        return sn_list, True


def try_split(sn_list):
    for k in range(len(sn_list)):
        if isinstance(sn_list[k], int) and sn_list[k] >= 10:
            sn_list[k:k+1] = ['[', sn_list[k]//2, int(ceil(sn_list[k]/2)), ']']
            return sn_list, True
    return sn_list, False


def add(sn1, sn2):
    return ['['] + sn1 + sn2 + [']']


def reduce(sn_list):
    while True:
        sn_list, changed = try_explode(sn_list)
        if changed:
            pass
            # print('explode', sn_list)
        else:
            sn_list, changed = try_split(sn_list)
            if changed:
                pass
                # print('split', sn_list)
            else:
                return sn_list


def add_list(lines):
    sn = add(to_list(lines[0]), to_list(lines[1]))
    k = 3
    while k < len(lines):
        sn = reduce(add(sn, to_list(lines[k])))
        k += 1
    return sn


def get_magnitude(sn_list):
    while len(sn_list) > 1:
        for k in range(len(sn_list) - 1):
            if isinstance(sn_list[k], int) and isinstance(sn_list[k+1], int):
                sn_list[k-1:k+3] = [3*sn_list[k] + 2*sn_list[k+1]]
                break
    return sn_list[0]


print(get_magnitude(add_list(lines)))

max_mag = -1
max_addends = None
for m in range(len(lines)):
    for n in range(len(lines)):
        if m != n:
            res = reduce(add(to_list(lines[m]), to_list(lines[n])))
            mag = get_magnitude(res)
            if mag > max_mag:
                max_mag = mag
                max_addends = (lines[m], lines[n], res)
print(max_mag)
# print(max_addends)

###########
# tests
###########
test1 = '[[[[[9,8],1],2],3],4]'
test2 = '[7,[6,[5,[4,[3,2]]]]]'
test3 = '[[6,[5,[4,[3,2]]]],1]'
test4 = '[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]'
# print(try_explode(to_list(test2)))

test5 = '[[[[4,3],4],4],[7,[[8,4],9]]]'
# print(reduce(add(to_list(test5), ['[', 1, 1, ']'])))
# print(add_test(6))


def add_test(maxn):
    sn = add(['[', 1, 1, ']'], ['[', 2, 2, ']'])
    n = 3
    while n <= maxn:
        sn = reduce(add(sn, ['[', n, n, ']']))
        print(sn)
        n += 1
    return sn


test6 = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]"""
# print(add_list(test6.splitlines()))
test9 = '[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]'
# print(get_magnitude(to_list(test9)))
# lines = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
# [[[5,[2,8]],4],[5,[[9,9],0]]]
# [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
# [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
# [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
# [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
# [[[[5,4],[7,7]],8],[[8,3],8]]
# [[9,3],[[9,9],[6,[4,9]]]]
# [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
# [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]""".splitlines()