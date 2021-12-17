# this problem feels a lot like a project euler problem - do some math to limit your search space before searching and accumulating some value as an answer...

import parse

file1 = open('day_17_input.txt', 'r')
lines = file1.read().strip()
# lines = 'target area: x=20..30, y=-10..-5'

format_str = 'target area: x={:d}..{:d}, y={:d}..{:d}'
x1,x2, y1,y2 = parse.parse(format_str, lines)
# print(x1,x2,y1,y2)


def hits_target(vx0, vy0, target):
    x1, x2, y1, y2 = target
    x = 0
    y = 0
    vx = vx0
    vy = vy0
    ymax = -100000
    while True:
        if y > ymax:
            ymax = y
        if x1 <= x <= x2 and y1 <= y <= y2:
            return True, ymax
        if vy < 0 and y < y1:
            return False, ymax
        if vx == 0 and (x < x1 or x > x2):
            return False, ymax
        x += vx
        y += vy
        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1
        vy -= 1

# print(hits_target(6, 9, (x1, x2, y1, y2)))

xmax_check = x2
ymax_abs = max(abs(y1), abs(y2))
ymax_check = 2*ymax_abs-1  # I have shown that there will not be solutions for vy0 > 2 * max(abs(y1), abs(y2)) - 3/4
# basically if y is a target y-value and y[n] is the y-height after n steps, then we have
# n = vy0 + 1/2 + sqrt((2 vy0 + 1)^2 - 8y), and we must require the quantity under the square root to be a square.
# We can acquire a bound from the size of differences of squares.

ymax_all = -1000000
high_v = None
count = 0
for vx in range(1, xmax_check+1):
    for vy in range(y1, ymax_check+1):
        hit, ymax = hits_target(vx, vy, (x1, x2, y1, y2))
        if hit:
            count += 1
            if ymax > ymax_all:
                ymax_all = ymax
                high_v = (vx, vy)
print(ymax_all)
# print(high_v)
print(count)
