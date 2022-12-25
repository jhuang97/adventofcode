import numpy as np
import matplotlib.pyplot as plt
import heapq
from collections import defaultdict

file = open('day24_in.txt', 'r')
# file = open('day24_test.txt', 'r')
# file = open('day24_test2.txt', 'r')
lines = file.read().strip().splitlines()
nr, nc = len(lines)-2, len(lines[0])-2
period = np.lcm(nr, nc)
# print(nr, nc, period)

blizzards = []
xstart = None
xend = None
for k, c in enumerate(lines[0]):
	if c == '.':
		xstart = k-1
for k, c in enumerate(lines[-1]):
	if c == '.':
		xend = k-1
for ir, l in enumerate(lines):
	for ic, c in enumerate(l):
		if c == '>':
			blizzards.append((ir-1, ic-1, 0, 1))
		if c == '<':
			blizzards.append((ir-1, ic-1, 0, -1))
		if c == 'v':
			blizzards.append((ir-1, ic-1, 1, 0))
		if c == '^':
			blizzards.append((ir-1, ic-1, -1, 0))

safe = np.ones((period, nr, nc), dtype=int)
for r0, c0, dr, dc in blizzards:
	if dr == 0: # period nc
		for k in range(nc):
			safe[k::nc, r0, (c0 + dc*k) % nc] = 0
	if dc == 0: # period nr
		for k in range(nr):
			safe[k::nr, (r0 + dr*k) % nr, c0] = 0

directions = [(-1, 0), (1, 0), (0, 1), (0, -1), (0,0)]
start_pos = (-1, xstart)
end_pos = (nr, xend)


def h_neighbor_fn(u, arr):
    a_shape = np.shape(arr)
    out = []
    t, r, c = u
    t2 = (t+1) % a_shape[0]
    for dr, dc in directions:
        r2 = r+dr
        c2 = c+dc
        if (0 <= r2 < a_shape[1] and 0 <= c2 < a_shape[2] and arr[t2, r2, c2]) or ((r2, c2) in [start_pos, end_pos]):
            out.append((t2, r2, c2))
    return out


def length_fn(u, v, arr):
    return 1


def manhattan(pt1, pt2):
    r1, c1 = pt1
    r2, c2 = pt2
    return abs(r1 - r2) + abs(c1 - c2)


class Node(object):
    def __init__(self, pt, val):
        self.pt = pt
        self.val = val

    def __repr__(self):
        return f'Node value: {self.val}'

    def __lt__(self, other):
        return self.val < other.val

    def __eq__(self, other):
        return self.pt == other.pt


def a_star_with_time(start, goal, arr, heuristic_fn, neighbor_fn, length_fn):
    came_from = {}
    g_score = defaultdict(lambda: np.inf)
    g_score[start] = 0
    f_score = defaultdict(lambda: np.inf)
    f_score[start] = heuristic_fn(start[1:], goal)
    Q = [Node(start, f_score[start])]
    heapq.heapify(Q)

    while Q:
        curr = heapq.heappop(Q).pt
        if curr[1:] == goal:
            return g_score[curr]

        # print(neighbor_fn(curr, arr))
        for v in neighbor_fn(curr, arr):
            tentative_g = g_score[curr] + length_fn(curr, v, arr)
            if tentative_g < g_score[v]:
                came_from[v] = curr
                g_score[v] = tentative_g
                f_score[v] = tentative_g + heuristic_fn(v[1:], goal)
                if Node(v, 0) not in Q:
                    heapq.heappush(Q, Node(v, f_score[v]))


# for k in range(period):
# 	print(k)
# 	print(safe[k, :, :])
t1 = a_star_with_time((0,) + start_pos, end_pos, safe, manhattan, h_neighbor_fn, length_fn)
print(t1)
t2 = a_star_with_time((t1,) + end_pos, start_pos, safe, manhattan, h_neighbor_fn, length_fn)
# print(t2)
t3 = a_star_with_time((t1+t2,) + start_pos, end_pos, safe, manhattan, h_neighbor_fn, length_fn)
# print(t3)

print(t1+t2+t3)