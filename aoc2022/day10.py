file1 = open('day10_in.txt', 'r')
# file1 = open('day10_test.txt', 'r')
lines = file1.read().strip().split('\n')

total = 0
tsave = [20, 60, 100, 140, 180, 220]

total = 0
t = 0
x = 1
for idx, l in enumerate(lines):
    t += 1
    pos = (t - 1) % 40
    print('#' if abs(x - pos) <= 1 else '.', end='\n' if pos == 39 else '')
    if t in tsave:
        total += t*x
        # print(t, x)
    if l.startswith('addx'):
        parts = l.split()
        dx = int(parts[1])
        t += 1
        pos = (t - 1) % 40
        print('#' if abs(x - pos) <= 1 else '.', end='\n' if pos == 39 else '')
        if t in tsave:
            total += t*x
            # print(t, x, idx, l)
        x += dx

print(total)