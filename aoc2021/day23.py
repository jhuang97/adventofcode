import heapq
import numpy as np
from collections import defaultdict
from copy import deepcopy

fname = 'day_23_input.txt'
# fname = 'day_23_test.txt'
file1 = open(fname, 'r')
lines = file1.read().strip().splitlines()

hw_start = lines[1].find('.', 0)
hw_end = lines[1].rfind('.')
hw_len = hw_end - hw_start + 1
slot_idx = []
for k in range(len(lines[2])):
    if lines[2][k].isalpha():
        slot_idx.append(k - hw_start)

print(slot_idx)

slot_states = []
for k in range(len(slot_idx)):  # 0th is inner, 1st is outer
    this_slot = [lines[3][slot_idx[k] + hw_start], lines[2][slot_idx[k] + hw_start]]
    slot_states.append(this_slot.copy())

blank_hw = ['.'] * hw_len


def state_to_str(hw, slot_states):
    s = ''.join(hw)
    for s2 in slot_states:
        s += ''.join(s2)
    return s


def str_to_state(s):
    hw = list(s[:hw_len])
    slot_states = []
    for k in range(len(slot_idx)):
        slot_states.append([s[hw_len + 2*k], s[hw_len + 2*k + 1]])
    return hw, slot_states



def dijkstra(start, end, legal_moves_fn):
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

        if u == end:
            return dist[u]
        explored.add(u)
        for v, cost in legal_moves_fn(u):
            alt = dist[u] + cost
            if v not in explored and v not in Q:
                Q.append(v)
                dist[v] = alt
            elif v in Q and alt < dist[v]:
                dist[v] = alt



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



# seems unnecessary to have used a heap for this
def a_star(start, goal, heuristic_fn, legal_moves_fn):
    came_from = {}
    g_score = defaultdict(lambda: np.inf)
    g_score[start] = 0
    f_score = defaultdict(lambda: np.inf)
    f_score[start] = heuristic_fn(start)
    Q = [Node(start, f_score[start])]
    heapq.heapify(Q)

    while Q:
        curr = heapq.heappop(Q).pt
        if curr == goal:
            return g_score[curr]

        for v, cost in legal_moves_fn(curr):
            tentative_g = g_score[curr] + cost
            if tentative_g < g_score[v]:
                came_from[v] = curr
                g_score[v] = tentative_g
                f_score[v] = tentative_g + heuristic_fn(v)
                if Node(v, 0) not in Q:
                    heapq.heappush(Q, Node(v, f_score[v]))



letter_idx = {'A':0, 'B':1, 'C':2, 'D':3}
per_cost = {'A':1, 'B':10, 'C':100, 'D':1000}


def legal_moves_fn(u):
    hw, slot_states = str_to_state(u)
    # take out; 0th is inner, 1st is outer
    moves = []
    for slotk in range(len(slot_idx)):
        from_idx = -1
        if slot_states[slotk][1].isalpha():
            from_idx = 1
        elif slot_states[slotk][0].isalpha():
            from_idx = 0
        if from_idx != -1:
            up_dist = 2 - from_idx
            pod_name = slot_states[slotk][from_idx]
            new_slot_states = deepcopy(slot_states)
            new_slot_states[slotk][from_idx] = '.'
            this_slot_idx = slot_idx[slotk]
            for k in range(this_slot_idx+1, hw_len):
                if hw[k] == '.':
                    if k not in slot_idx:
                        tot_dist = up_dist + k - this_slot_idx
                        new_hw = hw.copy()
                        new_hw[k] = pod_name
                        moves.append((state_to_str(new_hw, new_slot_states), tot_dist * per_cost[pod_name]))
                else:
                    break
            for k in range(this_slot_idx-1, -1, -1):
                if hw[k] == '.':
                    if k not in slot_idx:
                        tot_dist = up_dist + this_slot_idx - k
                        new_hw = hw.copy()
                        new_hw[k] = pod_name
                        moves.append((state_to_str(new_hw, new_slot_states), tot_dist * per_cost[pod_name]))
                else:
                    break

    # go in
    for k in range(hw_len):
        if hw[k].isalpha():
            pod_name = hw[k]
            # check if slot is suitable
            slotk = letter_idx[hw[k]]
            slotx = slot_idx[slotk]
            if slotx > k:
                vel = 1
            else:
                vel = -1
            k_check = k + vel
            blocked = False
            while True:
                if hw[k_check].isalpha():
                    blocked = True
                    break
                if k_check == slotx:
                    break
                k_check += vel
            if blocked:
                continue

            hw_dist = abs(slotx - k)

            c1 = slot_states[slotk][1]
            c0 = slot_states[slotk][0]
            if (c0 != '.' and c0 != hw[k]) or (c1 != '.' and c1 != hw[k]):
                continue
            inner_idx = 2
            if c1 == '.':
                inner_idx = 1
                if c0 == '.':
                    inner_idx = 0
            assert(inner_idx < 2)
            new_hw = hw.copy()
            new_slot_states = deepcopy(slot_states)
            new_slot_states[slotk][inner_idx] = pod_name
            new_hw[k] = '.'
            tot_dist = hw_dist + 2-inner_idx
            moves.append((state_to_str(new_hw, new_slot_states), tot_dist * per_cost[pod_name]))
    return moves


def heuristic_fn(u):
    hw, slot_states = str_to_state(u)
    tot_cost = 0
    for letter in ['A', 'B', 'C', 'D']:
        tot_dist = 0
        goal_slotk = letter_idx[letter]
        slotx = slot_idx[goal_slotk]
        for k in range(hw_len):  # amphipods in the hallway
            if hw[k] == letter:
                tot_dist += abs(k - slotx) + 2
        for slotk in range(len(slot_idx)):
            for sidx in [0, 1]:
                if slot_states[slotk][sidx] == letter:
                    if slotk == goal_slotk:
                        tot_dist += sidx
                    else:
                        tot_dist += (2-sidx) + abs(slotx - slot_idx[slotk]) + 2
        tot_cost += (tot_dist-1) * per_cost[letter]
    return tot_cost



# print(state_to_str(hw, slot_states))
# for idea in legal_moves_fn('...B.D.....AB..CCAD'):
# # for idea in legal_moves_fn(state_to_str(hw, slot_states)):
#     print(idea)
# print(str_to_state(state_to_str(hw, slot_states)))


# print(hw_start, hw_end)
# print(lines)
# print(slot_states)

print(heuristic_fn('.'*hw_len + 'AABBCCDD'))
print(heuristic_fn('.'*hw_len + 'CCBBAADD'))
# print(dijkstra(state_to_str(blank_hw, slot_states), '.'*hw_len + 'AABBCCDD', legal_moves_fn))

print(a_star(state_to_str(blank_hw, slot_states), '.'*hw_len + 'AABBCCDD', heuristic_fn, legal_moves_fn))