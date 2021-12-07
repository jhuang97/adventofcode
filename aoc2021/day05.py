import numpy as np

file1 = open('day_5_input.txt', 'r')
lines = file1.read().strip().split('\n')
x1s = []
y1s = []
x2s = []
y2s = []
for l in lines:
    pairs = l.split(' -> ')
    pair1 = pairs[0].split(',')
    pair2 = pairs[1].split(',')
    x1s.append(int(pair1[0]))
    y1s.append(int(pair1[1]))
    x2s.append(int(pair2[0]))
    y2s.append(int(pair2[1]))
# print(min(x1s + x2s))
# print(min(y1s + y2s))
xsize = max(x1s+x2s)+1
ysize = max(y1s+y2s)+1

overlaps = np.zeros((xsize, ysize))
for k in range(len(x1s)):
    if x1s[k] == x2s[k]:
        y1 = min(y1s[k], y2s[k])
        y2 = max(y1s[k], y2s[k])
        overlaps[x1s[k], y1:(y2+1)] += 1
    elif y1s[k] == y2s[k]:
        x1 = min(x1s[k], x2s[k])
        x2 = max(x1s[k], x2s[k])
        overlaps[x1:(x2+1), y1s[k]] += 1

print(np.sum(overlaps >= 2))

overlaps = np.zeros((xsize, ysize))
for k in range(len(x1s)):
    if x1s[k] == x2s[k]:
        y1 = min(y1s[k], y2s[k])
        y2 = max(y1s[k], y2s[k])
        overlaps[x1s[k], y1:(y2+1)] += 1
    elif y1s[k] == y2s[k]:
        x1 = min(x1s[k], x2s[k])
        x2 = max(x1s[k], x2s[k])
        overlaps[x1:(x2+1), y1s[k]] += 1
    else:
        xdir = 1 if x2s[k] > x1s[k] else -1
        ydir = 1 if y2s[k] > y1s[k] else -1
        x = x1s[k]
        y = y1s[k]
        while True:
            overlaps[x, y] += 1
            if x == x2s[k]:
                break
            x += xdir
            y += ydir

print(np.sum(overlaps >= 2))
