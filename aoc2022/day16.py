import itertools
import numpy as np
from collections import defaultdict

file = open('day16_in.txt', 'r')
# file = open('day16_test.txt', 'r')
lines = file.read().strip().splitlines()


def expect_s(s, expect):
    if not s.startswith(expect):
        print('oh no', s, expect)
    return s[len(expect):]


nz_valves = []
neighbors = defaultdict(list)
rates = {}
for l in lines:
    s = expect_s(l, 'Valve ')
    vname, s = s[:2], s[2:]
    s = expect_s(s, ' has flow rate=')
    if 'valves' in s:
        parts = s.split('; tunnels lead to valves ')
    else:
        parts = s.split('; tunnel leads to valve ')
    rate = int(parts[0])
    rates[vname] = rate
    if rate > 0:
        nz_valves.append(vname)
    nbs = parts[1].split(', ')
    for nb in nbs:
        neighbors[vname].append(nb)

# print(nz_valves, len(nz_valves))
# print(rates)
# print(neighbors)

nodes = ['AA'] + nz_valves


def dijkstra_to_multiple(start, ends, legal_moves_fn):
    dist = {} # defaultdict(lambda: float('inf'))
    Q = [start]
    dist[start] = 0
    explored = set()

    while Q:
        min_dist = float('inf')
        u = Q[0]
        for v in Q:
            if dist[v] < min_dist:
                min_dist = dist[v]
                u = v

        Q.remove(u)
        # print(len(Q))

        if u in ends:
            ends.remove(u)
        if len(ends) == 0:
            return dist
        explored.add(u)
        for v, cost in legal_moves_fn(u):
            alt = dist[u] + cost
            if v not in explored and v not in Q:
                Q.append(v)
                dist[v] = alt
            elif v in Q and alt < dist[v]:
                dist[v] = alt


pair_dists = {}
for n in nodes:
    other_nodes = nodes.copy()
    other_nodes.remove(n)
    pair_dists[n] = dijkstra_to_multiple(n, other_nodes, lambda x: [(nb, 1) for nb in neighbors[x]])


# arr = np.zeros((len(nodes), len(nodes)), dtype=int)
# for k1 in range(len(nodes)):
#     for k2 in range(len(nodes)):
#         arr[k1, k2] = pair_dists[nodes[k1]][nodes[k2]]
# print(arr)

# try greedy
pos = 'AA'
tleft = 30
ptotal = 0
opened = ['AA']


def get_best_p_nodes(state, nodes):
    pos, tleft, ptotal, opened = state

    best_p = ptotal
    for n in nodes:
        if n not in opened:
            dist = pair_dists[pos][n]
            if dist+1 < tleft:
                p_all = rates[n] * (tleft - dist - 1)
                o_new = opened.copy()
                o_new.append(n)
                this_p = get_best_p_nodes((n, tleft-dist-1, ptotal+p_all, o_new), nodes)
                if this_p > best_p:
                    best_p = this_p
        # print(pos, best_n)
    return best_p


print(get_best_p_nodes(('AA', 30, 0, ['AA']), nodes))


best_p = 0
for nchoose in range(1, len(nz_valves)//2+1):
    for k in itertools.combinations(nz_valves, nchoose):
        nodes1 = list(k)
        nodes2 = [v for v in nz_valves if v not in k]
        this_p = get_best_p_nodes(('AA', 26, 0, ['AA']), nodes1) + get_best_p_nodes(('AA', 26, 0, ['AA']), nodes2)
        if this_p > best_p:
            best_p = this_p
    print(nchoose, best_p)
print(best_p)