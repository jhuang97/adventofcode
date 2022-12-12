import numpy as np
import heapq
from collections import defaultdict

file1 = open('day12_in.txt', 'r')
lines = file1.read().strip().splitlines()


def get_height(c):
    if c == 'S':
        d = 'a'
    elif c == 'E':
        d = 'z'
    else:
        d = c
    return ord(d) - ord('a')


def h_neighbor_fn(u, arr):
    a_shape = np.shape(arr)
    out = []
    r, c = u
    for dr, dc in directions:
        r2 = r+dr
        c2 = c+dc
        if 0 <= r2 < a_shape[0] and 0 <= c2 < a_shape[1]:
            dh = arr[r2, c2] - arr[r, c]
            if dh <= 1:
                out.append((r2, c2))
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

heights = []
for l in lines:
    heights.append([get_height(c) for c in l])
heights = np.array(heights)
directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]


def a_star(start, goal, arr, heuristic_fn, neighbor_fn, length_fn):
    came_from = {}
    g_score = defaultdict(lambda: np.inf)
    g_score[start] = 0
    f_score = defaultdict(lambda: np.inf)
    f_score[start] = heuristic_fn(start, goal)
    Q = [Node(start, f_score[start])]
    heapq.heapify(Q)

    while Q:
        curr = heapq.heappop(Q).pt
        if curr == goal:
            return g_score[curr]

        for v in neighbor_fn(curr, arr):
            tentative_g = g_score[curr] + length_fn(curr, v, arr)
            if tentative_g < g_score[v]:
                came_from[v] = curr
                g_score[v] = tentative_g
                f_score[v] = tentative_g + heuristic_fn(v, goal)
                if Node(v, 0) not in Q:
                    heapq.heappush(Q, Node(v, f_score[v]))


nr, nc = np.shape(heights)
for r in range(nr):
    for c in range(nc):
        if lines[r][c] == 'S':
            start = (r, c)
        if lines[r][c] == 'E':
            dest = (r, c)
print(a_star(start, dest, heights, manhattan, h_neighbor_fn, length_fn))

min_a_dist = nr*nc
for r in range(nr):
    for c in range(nc):
        if heights[r, c] == 0:
            dist = a_star((r, c), dest, heights, manhattan, h_neighbor_fn, length_fn)
            if dist is None:
                # print((r,c))
                continue
            if dist < min_a_dist:
                min_a_dist = dist
print(min_a_dist)