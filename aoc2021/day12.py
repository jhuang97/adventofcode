from collections import defaultdict

file1 = open('day_12_input.txt', 'r')
lines = file1.read().strip().split('\n')
# lines = """dc-end
# HN-start
# start-kj
# dc-start
# dc-HN
# LN-dc
# HN-end
# kj-sa
# kj-HN
# kj-dc""".splitlines()

neighbors = defaultdict(list)
for l in lines:
    parts = l.split('-')
    neighbors[parts[0]].append(parts[1])
    neighbors[parts[1]].append(parts[0])


def num_ways(path):
    node = path[-1]
    total = 0
    for n in neighbors[node]:
        if n == 'end':
            total += 1
        elif n.isupper() or (n.islower() and n not in path):
            total += num_ways(path + (n,))
    return total


print(num_ways(('start',)))


def num_ways_2(path, small_twice):
    node = path[-1]
    total = 0
    for n in neighbors[node]:
        if n == 'end':
            total += 1
        elif n.isupper():
            total += num_ways_2(path + (n,), small_twice)
        elif n.islower() and n != 'start':
            if n in path:
                if not small_twice:
                    total += num_ways_2(path + (n,), True)
            else:
                total += num_ways_2(path + (n,), small_twice)
    return total


print(num_ways_2(('start',), False))


def iterative_DFS():
    n_ways = 0
    path_indices = []
    path = ['start']
    node = path[-1]
    num_neighbors = len(neighbors[node])
    child_idx = 0
    while True:
        if child_idx < num_neighbors:
            node2 = neighbors[node][child_idx]
            if node2 == 'end':
                n_ways += 1
                child_idx += 1
            elif node2.isupper() or (node2.islower() and node2 not in path):
                path.append(node2)
                path_indices.append(child_idx)
                node = node2
                num_neighbors = len(neighbors[node])
                child_idx = 0
            else:
                child_idx += 1
        else:
            if len(path) > 1:
                path.pop()
                node = path[-1]
                num_neighbors = len(neighbors[node])
                child_idx = path_indices.pop() + 1
            else:
                break
    return n_ways


print(iterative_DFS())


def iterative_DFS_2():
    n_ways = 0
    path_indices = []
    repeat_small = []
    path = ['start']
    node = path[-1]
    num_neighbors = len(neighbors[node])
    child_idx = 0
    while True:
        if child_idx < num_neighbors:
            step_in = False
            node2 = neighbors[node][child_idx]
            if node2 == 'end':
                n_ways += 1
                child_idx += 1
            elif node2.isupper():
                step_in = True
                repeat_small.append(False)
            elif node2.islower() and node2 != 'start':
                if node2 in path:
                    if True in repeat_small:
                        child_idx += 1
                    else:
                        step_in = True
                        repeat_small.append(True)
                else:
                    step_in = True
                    repeat_small.append(False)
            else:
                child_idx += 1
            if step_in:
                path.append(node2)
                path_indices.append(child_idx)
                node = node2
                num_neighbors = len(neighbors[node])
                child_idx = 0
        else:
            if len(path) > 1:
                path.pop()
                node = path[-1]
                num_neighbors = len(neighbors[node])
                child_idx = path_indices.pop() + 1
                repeat_small.pop()
            else:
                break
    return n_ways


print(iterative_DFS_2())
