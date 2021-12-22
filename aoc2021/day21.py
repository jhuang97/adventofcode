fname = 'day_21_input.txt'
file1 = open(fname, 'r')
lines = file1.read().strip().splitlines()

start_pos = []
for l in lines:
    start_pos.append(int(l.split(': ')[1]))
# start_pos = [4,8]

die_rolls = 0
die_idx = 1
scores = [0, 0]
turn = 0
state = (start_pos.copy(), scores.copy(), die_rolls, die_idx, turn)


def update(state):
    pos, scores, n_rolls, die_idx, turn = state
    die_value = 0
    for k in range(3):
        die_value += die_idx
        die_idx += 1
        if die_idx > 100:
            die_idx = 1
    n_rolls += 3
    pos[turn] = ((pos[turn] + die_value - 1) % 10) + 1
    scores[turn] += pos[turn]
    turn = 1-turn
    return pos, scores, n_rolls, die_idx, turn


win = False
win_idx = -1
while not win:
    state = update(state)
    # print(state)
    if state[1][0] >= 1000:
        win_idx = 0
        win = True
    elif state[1][1] >= 1000:
        win_idx = 1
        win = True
print(state[1][1-win_idx] * state[2])

n_branch = [0, 0, 0, 1, 3, 6, 7, 6, 3, 1]

memo = {}


def count_wins(pos, scores, turn):
    state = (pos[0], pos[1], scores[0], scores[1], turn)
    if state in memo:
        return memo[state]

    wins = [0, 0]
    for k in range(3, 10):
        new_pos = ((pos[turn] + k - 1) % 10) + 1
        new_score = scores[turn] + new_pos
        if new_score >= 21:
            wins[turn] += n_branch[k]
        else:
            new_pos_list = pos.copy()
            new_pos_list[turn] = new_pos
            new_score_list = scores.copy()
            new_score_list[turn] = new_score
            result = count_wins(new_pos_list, new_score_list, 1-turn)
            wins[0] += n_branch[k] * result[0]
            wins[1] += n_branch[k] * result[1]

    memo[state] = wins
    return wins


print(max(count_wins(start_pos, [0, 0], 0)))
# print(len(memo))