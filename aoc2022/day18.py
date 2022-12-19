import numpy as np

file = open('day18_in.txt', 'r')
# file = open('day18_test.txt', 'r')
lines = file.read().strip().splitlines()
arr = np.array([[int(n) for n in l.split(',')] for l in lines])

pt_set = set()
for k in arr:
    pt_set.add(tuple(k))


air_set = set()
total = 0
for d in range(3):
    for delta in [-1, 1]:
        darr = arr.copy()
        darr[:, d] += delta
        for k in darr:
            m_pt = tuple(k)
            if m_pt not in pt_set:
                air_set.add(m_pt)
                total += 1
print(total)

bounds = (np.min(arr, axis=0), np.max(arr, axis=0))
bounds2 = (bounds[0]-1, bounds[1]+1)
# print(bounds)
# print(len(arr), len(air_set))


def get_nb_air(coords):
    c = np.array(list(coords))
    out = []
    for d in range(3):
        for delta in [-1, 1]:
            darr = c.copy()
            darr[d] += delta
            # print(darr)
            dt = tuple(darr)
            if (not np.any(darr < bounds2[0])) and (not np.any(darr > bounds2[1])) and (dt not in pt_set):
                out.append((tuple(dt), 1))
    return out


def try_dijkstra_to_multiple(start, ends, legal_moves_fn):
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
        explored.add(u)
        for v, cost in legal_moves_fn(u):
            alt = dist[u] + cost
            if v not in explored and v not in Q:
                Q.append(v)
                dist[v] = alt
            elif v in Q and alt < dist[v]:
                dist[v] = alt
    return ends


unreachable_air_set = try_dijkstra_to_multiple(tuple(bounds2[0]), air_set, get_nb_air)
# print(len(unreachable_air_set))

ext_air_set = set()
total = 0
for d in range(3):
    for delta in [-1, 1]:
        darr = arr.copy()
        darr[:, d] += delta
        for k in darr:
            m_pt = tuple(k)
            if m_pt not in pt_set and m_pt not in unreachable_air_set:
                ext_air_set.add(m_pt)
                total += 1
print(total)