file1 = open('day03_in.txt', 'r')
lines = file1.read().strip().split('\n')


def priority(c):
    o = ord(c)
    if o > ord('Z'):  # lowercase
        return o-ord('a') + 1
    else:  # uppercase
        return o-ord('A') + 27


total = 0
for l in lines:
    half_len = len(l)//2
    a, b = l[:half_len], l[half_len:]
    for c in a:
        if c in b:
            total += priority(c)
            # print(a, b, c)
            break
print(total)

n_lines = len(lines)
n_groups = n_lines//3

total = 0
for k in range(n_groups):
    x, y, z = lines[3*k], lines[3*k+1], lines[3*k+2]
    for c in x:
        if c in y and c in z:
            total += priority(c)
            # print(x,y,z,c)
            break
print(total)