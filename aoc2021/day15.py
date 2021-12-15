import numpy as np
import heapq
from collections import defaultdict

file1 = open('day_15_input.txt', 'r')
lines = file1.read().strip().split('\n')
# lines = """1163751742
# 1381373672
# 2136511328
# 3694931569
# 7463417111
# 1319128137
# 1359912421
# 3125421639
# 1293138521
# 2311944581""".splitlines()

risks = []
for l in lines:
    risks.append([int(c) for c in list(l)])

risks = np.array(risks)
directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]


def risks_neighbor_fn(u, arr):
    a_shape = np.shape(arr)
    out = []
    r, c = u
    for dr, dc in directions:
        r2 = r+dr
        c2 = c+dc
        if 0 <= r2 < a_shape[0] and 0 <= c2 < a_shape[1]:
            out.append((r2, c2))
    return out


def risks_length_fn(u, v, arr):
    r, c = v
    return arr[r, c]


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


def dijkstra(start, end, arr, vertices, neighbor_fn, length_fn):
    dist = {}
    Q = vertices.copy()
    for v in vertices:
        dist[v] = np.Inf
    dist[start] = 0

    while Q:
        min_dist = np.Inf
        u = Q[0]
        for v in Q:
            if dist[v] < min_dist:
                min_dist = dist[v]
                u = v

        Q.remove(u)
        # print(len(Q))

        if u == end:
            return dist[u]
        for v in neighbor_fn(u, arr):
            if v in Q:
                alt = dist[u] + length_fn(u, v, arr)
                if alt < dist[v]:
                    dist[v] = alt


def manhattan(pt1, pt2):
    r1, c1 = pt1
    r2, c2 = pt2
    return abs(r1 - r2) + abs(c1 - c2)


# seems unnecessary to have used a heap for this
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


n_rows, n_cols = np.shape(risks)
v_list = [(r, c) for r in range(n_rows) for c in range(n_cols)]
# print(dijkstra((0, 0), (n_rows-1, n_cols-1), risks, v_list, risks_neighbor_fn, risks_length_fn))
print(a_star((0, 0), (n_rows-1, n_cols-1), risks, manhattan, risks_neighbor_fn, risks_length_fn))

risks_big = np.zeros((n_rows*5, n_cols*5), dtype=int)
risks_big[:n_rows, :n_cols] = risks
ridx = n_rows * np.array(list(range(6)))
cidx = n_cols * np.array(list(range(6)))
for r in range(5):
    for c in range(5):
        if c > 0:
            risks_prev = risks_big[ridx[r]:ridx[r+1], cidx[c-1]:cidx[c]]
            risks_big[ridx[r]:ridx[r+1], cidx[c]:cidx[c+1]] = np.mod(risks_prev, 9) + 1
        elif r > 0:
            risks_prev = risks_big[ridx[r-1]:ridx[r], cidx[c]:cidx[c+1]]
            risks_big[ridx[r]:ridx[r + 1], cidx[c]:cidx[c + 1]] = np.mod(risks_prev, 9) + 1
print(a_star((0, 0), (n_rows*5-1, n_cols*5-1), risks_big, manhattan, risks_neighbor_fn, risks_length_fn))