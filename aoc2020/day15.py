file1 = open('day_15_input.txt', 'r')
nums = [int(w) for w in file1.read().split(',')]


def seq(start, maxlen):
    idx0 = len(start)
    for k in range(idx0, maxlen):
        if k % 10000 == 0:
            print(k)
        last = start[-1]
        if start.count(last) == 1:
            start.append(0)
        else:
            indices = [i for i, x in enumerate(start) if x == last]
            start.append(indices[-1] - indices[-2])
    return start[-1]


def seq2(start, maxlen):
    idx0 = len(start)
    recent = {}
    for i, x in enumerate(start):
        recent[x] = [i]
    last = start[-1]
    for k in range(idx0, maxlen):
        if k % 1000000 == 0:
            print(k)
        if len(recent[last]) == 1:
            curr = 0
        else:
            curr = recent[last][-1] - recent[last][-2]
        if curr not in recent:
            recent[curr] = [k]
        elif len(recent[curr]) == 1:
            recent[curr].append(k)
        else:
            recent[curr][0], recent[curr][1] = recent[curr][-1], k
        last = curr
    return last


print(seq(nums, 2020))
print(seq2(nums, 30000000))
