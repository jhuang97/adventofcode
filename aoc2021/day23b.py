import heapq
import numpy as np
from collections import defaultdict
from copy import deepcopy

fname = 'day_23_input.txt'
# fname = 'day_23_test.txt'
file1 = open(fname, 'r')
lines = file1.read().strip().splitlines()

lines = lines[0:3] + """  #D#C#B#A#
  #D#B#A#C#""".splitlines() + lines[3:]

hw_start = lines[1].find('.', 0)
hw_end = lines[1].rfind('.')
hw_len = hw_end - hw_start + 1
slot_idx = []
for k in range(len(lines[2])):
    if lines[2][k].isalpha():
        slot_idx.append(k - hw_start)

slot_states = []
for k in range(len(slot_idx)):  # 0th is innermost, 3rd is outermost
    this_slot = []
    for sidx in range(4):
        this_slot.append(lines[5-sidx][slot_idx[k] + hw_start])
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
        slot_states.append(list(s[(hw_len + 4*k):(hw_len + 4*(k+1))]))
    return hw, slot_states



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
                # if f_score[v] % 100 == 0:
                # print(f_score[v])
                if Node(v, 0) not in Q:
                    if (f_score[v] // 100) % 10 == 0:
                        print(v, f_score[v])
                    heapq.heappush(Q, Node(v, f_score[v]))



letter_idx = {'A':0, 'B':1, 'C':2, 'D':3}
per_cost = {'A':1, 'B':10, 'C':100, 'D':1000}


def legal_moves_fn(u):
    hw, slot_states = str_to_state(u)
    # take out
    moves = []
    for slotk in range(len(slot_idx)):
        from_idx = -1
        for sidx in range(4):
            if slot_states[slotk][sidx].isalpha():
                from_idx = sidx
        if from_idx != -1:
            up_dist = 4 - from_idx
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
            wrong_letter = False
            for c in slot_states[slotk]:
                if c != '.' and c != hw[k]:
                    wrong_letter = True
                    break
            if wrong_letter:
                continue
            inner_idx = 4
            for sidx in range(3, -1, -1):
                if slot_states[slotk][sidx] == '.':
                    inner_idx = sidx
                else:
                    break
            assert(inner_idx < 4)
            new_hw = hw.copy()
            new_slot_states = deepcopy(slot_states)
            new_slot_states[slotk][inner_idx] = pod_name
            new_hw[k] = '.'
            tot_dist = hw_dist + 4-inner_idx
            moves.append((state_to_str(new_hw, new_slot_states), tot_dist * per_cost[pod_name]))
    return moves



# memo = {}


def heuristic_fn(u):
    # if u in memo:
    #     return memo[u]
    hw, slot_states = str_to_state(u)
    tot_cost = 0
    for letter in ['A', 'B', 'C', 'D']:
        tot_dist = 0
        goal_slotk = letter_idx[letter]
        slotx = slot_idx[goal_slotk]

        goal_sidx = 0
        # first check amphipods in the right slot
        for sidx in range(4):
            if slot_states[goal_slotk][sidx] == letter:
                tot_dist += abs(goal_sidx - sidx)
                goal_sidx += 1
        # next check amphipods in the hallway
        for k in range(hw_len):  # amphipods in the hallway
            if hw[k] == letter:
                tot_dist += abs(k - slotx) + 4 - goal_sidx
                goal_sidx += 1
        for slotk in range(len(slot_idx)):
            if slotk != goal_slotk:
                for sidx in range(4):
                    if slot_states[slotk][sidx] == letter:
                        tot_dist += (4-sidx) + abs(slotx - slot_idx[slotk]) + 4-goal_sidx
                        goal_sidx += 1
        tot_cost += tot_dist * per_cost[letter]
    # memo[u] = tot_cost
    return tot_cost


# print(slot_states)
# print(state_to_str(blank_hw, slot_states))
# print(str_to_state(state_to_str(blank_hw, slot_states)))

# for idea in legal_moves_fn(state_to_str(blank_hw, slot_states)):
#     print(idea)
# print(heuristic_fn('.'*hw_len + 'AAAABBBBCCCCDDDD'))
# print(heuristic_fn('.'*hw_len + 'CCCCBBBBAAAADDDD'))
# print(a_star('.'*hw_len + 'CCAABBBBAACCDDDD', '.'*hw_len + 'AAAABBBBCCCCDDDD', heuristic_fn, legal_moves_fn))
# print(heuristic_fn(state_to_str(blank_hw, slot_states)))
print(a_star(state_to_str(blank_hw, slot_states), '.'*hw_len + 'AAAABBBBCCCCDDDD', heuristic_fn, legal_moves_fn))
# print(len(memo))