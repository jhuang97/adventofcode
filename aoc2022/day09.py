file1 = open('day09_in.txt', 'r')
lines = file1.read().strip().split('\n')

dirs = {'U': (0, 1), 'D': (0, -1), 'R': (1, 0), 'L': (-1, 0)}
backup_dirs = [(-1, 1), (1, 1), (1, -1), (-1, -1)]


def update_tail(old_tail, head):
    xo, yo = old_tail
    xh, yh = head
    if abs(xh-xo) <= 1 and abs(yh-yo) <= 1:
        return old_tail
    for dx, dy in dirs.values():
        xn, yn = xh+dx, yh+dy
        if abs(xn-xo) <= 1 and abs(yn-yo) <= 1:
            return xn, yn
    for dx, dy in backup_dirs:
        xn, yn = xh+dx, yh+dy
        if abs(xn-xo) <= 1 and abs(yn-yo) <= 1:
            return xn, yn
    print('oh no', old_tail, head)


visited = {(0, 0)}
head = (0, 0)
tail = (0, 0)
for l in lines:
    parts = l.split()
    dx, dy = dirs[parts[0]]
    steps = int(parts[1])

    for _ in range(steps):
        head = (head[0]+dx, head[1]+dy)
        tail = update_tail(tail, head)
        visited.add(tail)
print(len(visited))

rope = []
for _ in range(10):
    rope.append((0,0))
visited = {(0, 0)}

for l in lines:
    parts = l.split()
    dx, dy = dirs[parts[0]]
    steps = int(parts[1])

    for _ in range(steps):
        new_rope = [(rope[0][0] + dx, rope[0][1] + dy)]
        for k in range(1, 10):
            new_rope.append(update_tail(rope[k], new_rope[k-1]))
        visited.add(new_rope[-1])
        rope = new_rope
print(len(visited))