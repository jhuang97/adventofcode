import numpy as np

file = open('day19_in.txt', 'r')
# file = open('day19_test.txt', 'r')
lines = file.read().strip().splitlines()

resources = ['ore', 'clay', 'obsidian', 'geode']
r_id = {'ore':0, 'clay':1, 'obsidian':2, 'geode':3}


class Blueprint:
    def __init__(self, s):
        p = s.split(': ')
        self.id = int(p[0].split()[1])
        p = p[1].split('.')
        # print(p)

        self.rcosts = []
        for ss in p:
            if len(ss) > 0:
                parts = ss.split(' costs ')[1].split(' and ')
                cost_arr = [0] * 4
                for part in parts:
                    tokens = part.split()
                    cost_arr[r_id[tokens[1]]] = int(tokens[0])
                self.rcosts.append(np.array(cost_arr))

    def expand_state(self, st):
        res, robots = st
        res, robots = np.array(res), np.array(robots)
        res_available = res.copy()
        res_new = np.array(res) + np.array(robots)

        out = [(tuple(res_new), tuple(robots))]
        for k in range(4):
            if np.all(res_available >= self.rcosts[k]):
                robots_new = robots.copy()
                robots_new[k] += 1
                out.append((tuple(res_new - self.rcosts[k]), tuple(robots_new)))
        return out

    def G_est(self, st, dt):
        res, robots = st
        Gnow = res[3]
        _, nRC, nRO, nRG = robots
        return Gnow + nRG * dt + nRO * dt**2 / (2 * self.rcosts[3][2])\
            + nRC * dt**3 / (6 * self.rcosts[2][1] * self.rcosts[3][2])

    def beam_search(self, tmax, width):
        states = [((0, 0, 0, 0), (1, 0, 0, 0))]
        t = 0

        while t < tmax:
            next_states = set()
            for st in states:
                next_states.update(self.expand_state(st))
            next_states = list(next_states)
            scores = np.array([self.G_est(st, tmax-t) for st in next_states])
            s_index = np.argsort(scores)
            n_take = min(width, len(s_index))
            states = [next_states[sidx] for sidx in s_index[-n_take:]]

            t += 1

        most_g = 0
        for res, robots in states:
            if res[3] > most_g:
                most_g = res[3]

        return most_g


total = 0
for l in lines:
    b = Blueprint(l)
    res = b.beam_search(24, 2000)
    # print(b.id, res)
    total += b.id * res
print(total)


product = 1
for k in range(3):
    res = Blueprint(lines[k]).beam_search(32, 2000)
    product *= res
    # print(k, res)
print(product)


# Things I tried that were too slow

# import itertools

# some functions and stuff in class Blueprint:

# self.memo = {}

# def max_geodes_helper(self, tmax, t, res, robots):
#     # state = (tmax, t, tuple(res), tuple(robots))
#     # if state in self.memo:
#     #     return self.memo[state]
#
#     # print(t, res, robots)
#     res_available = res.copy()
#     # collect resources
#     res += robots
#
#     if t == tmax:
#         return res[3]
#
#     vals = [self.max_geodes_helper(tmax, t+1, res.copy(), robots.copy())]
#     for k in range(4):
#         if np.all(res_available >= self.rcosts[k]):
#             print('try buy', k, 'on round', t)
#             new_robots = robots.copy()
#             new_robots[k] += 1
#             vals.append(self.max_geodes_helper(tmax, t+1, res-self.rcosts[k], new_robots))
#     sol = max(vals)
#     # self.memo[state] = sol
#     return sol
#
# def max_geodes(self, tmax):
#     return self.max_geodes_helper(tmax, 1, np.array([0]*4), np.array([1, 0, 0, 0]))
#
# def min_time_for_g_robots(self, res, robots):
#     return self.min_time_helper(0, res, robots, [])
#
# def min_time_helper(self, t, res, robots, order):
#     if np.all(res >= self.rcosts[3]):
#         return t, order
#
#     res_available = res.copy()
#     # collect resources
#     res += robots
#
#     min_time, best_order = self.min_time_helper(t + 1, res.copy(), robots.copy(), order.copy())
#     for k in range(3):
#         if np.all(res_available >= self.rcosts[k]):
#             new_robots = robots.copy()
#             new_robots[k] += 1
#             m_time, m_order = self.min_time_helper(t+1, res-self.rcosts[k], new_robots, order.copy() + [k])
#             if m_time < min_time:
#                 min_time = m_time
#                 best_order = m_order
#     return min_time, best_order
#
# def try_build_order(self, tmax, order):
#     t = 1
#     res = np.array([0]*4)
#     robots = np.array([1, 0, 0, 0])
#     oidx = 0
#     curr_cost = self.rcosts[order[oidx]]
#     while True:
#         # print('minute', t, res, robots)
#         res_available = res.copy()
#         # collect resources
#         res += robots
#
#         if t >= tmax:
#             return res[3], oidx
#
#         # spent = np.array([0]*4)
#         if order[oidx] == 3 and robots[2] == 0:
#             return 0, oidx
#         if order[oidx] == 2 and robots[1] == 0:
#             return 0, oidx
#
#         if np.all(res_available >= curr_cost):
#             robots[order[oidx]] += 1
#             res -= curr_cost
#             # print(t, order[oidx], res, robots)
#             oidx += 1
#             curr_cost = self.rcosts[order[oidx]]
#
#         t += 1
#
# def build_order_search(self, tmax):
#     best_order = None
#     max_geodes = 0
#     # for order in itertools.product(range(1,4), repeat=12):
#     #     if order[0] <= 1:
#     #         ng, oidx = self.try_build_order(tmax, order)
#     #         if ng > max_geodes:
#     #             max_geodes = ng
#     #             best_order = order[:oidx]
#     for o1 in itertools.product(range(0,4), repeat=1):
#         for o2 in itertools.product(range(1, 4), repeat=13):
#             order = o1 + o2
#             print(order)
#             if order[0] <= 1:
#                 ng, oidx = self.try_build_order(tmax, order)
#                 if ng > max_geodes:
#                     max_geodes = ng
#                     best_order = order[:oidx]
#
#     return max_geodes, best_order

# print(b.id, b.rcosts)
# # print(b.max_geodes(24))
# print(b.min_time_for_g_robots(np.array([0]*3), np.array([1, 0, 0])))

# b.try_build_order(24, (1, 1, 1, 2, 1, 2, 3, 1, 3, 1))
# print(b.try_build_order(24, (1, 1, 1, 2, 1, 2, 3, 3,3,3,3,3)))

# print(b.build_order_search(24))