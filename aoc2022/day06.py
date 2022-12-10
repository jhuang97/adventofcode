file1 = open('day06_in.txt', 'r')
line = file1.read().strip()
# line = 'mjqjpqmgbljsphdztnvjfqwrcgsmlb'

for k in range(3, len(line)):
    if line[k] != line[k-1] and line[k] != line[k-2] and line[k] != line[k-3] and line[k-2] != line[k-1] and line[k-3] != line[k-1] and line[k-3] != line[k-2]:
        print(k+1)
        # print(line[:k+1])
        break


def distinct(s):
    chars = set()
    for c in s:
        if c not in chars:
            chars.add(c)
        else:
            return False
    return True


for k in range(14, len(line)):
    if distinct(line[k-14:k]):
        print(k)
        break