import itertools
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

file = open('day17_in.txt', 'r')
# file = open('day17_test.txt', 'r')
dirs = file.read().strip()
# dirs = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'

piece_def = [
    [(0,0), (0,1), (0,2), (0,3)],
    [(0,1), (1,0), (1,1), (2,1), (1,2)],
    [(0,0), (0,1), (0,2), (1,2), (2,2)],
    [(0,0), (1,0), (2,0), (3,0)],
    [(0,0), (1,0), (0,1), (1,1)]
]  # (y, x)
npiece = len(piece_def)


def show(board):
    for l in reversed(board):
        out = '|'
        for c in l:
            out += '#' if c == 1 else '.'
        print(out + '|')


board = []
w = 7
piece_idx = 0
dir_idx = 0
nd = len(dirs)
nstop = 0
curr_piece = None
px, py = None, None

ht_rec = [0]

full_n = []
full_ht = []

while nstop < 28e3:
    if curr_piece is None: # spawn
        curr_piece = piece_idx
        piece_idx = (piece_idx + 1) % npiece
        px, py = 2, len(board)+3
    else:
        curr_d = dirs[dir_idx]
        dir_idx = (dir_idx + 1) % nd
        # try curr_d
        px_test = px + (-1 if curr_d == '<' else 1)
        works = True
        for dy, dx in piece_def[curr_piece]:
            tx = px_test + dx
            if tx >= w or tx < 0:
                works = False
                break
            ty = py + dy
            if ty < len(board):
                if board[ty][tx] != 0:
                    works = False
                    break
        if works:
            px = px_test

        # try fall
        py_test = py - 1
        works = True
        for dy, dx in piece_def[curr_piece]:
            tx = px + dx
            ty = py_test + dy
            if ty < 0:
                works = False
                break
            if ty < len(board):
                if board[ty][tx] != 0:
                    works = False
                    break
        if works:
            py = py_test
        else:  # rock stops
            full_line = None
            for dy, dx in piece_def[curr_piece]:
                tx = px + dx
                ty = py + dy
                while ty >= len(board):
                    board.append([0]*7)
                board[ty][tx] = 1
                if board[ty].count(1) == w:
                    full_line = ty
            nstop += 1
            curr_piece = None

            if full_line is not None:
                full_ht.append(len(board))
                full_n.append(nstop)

            ht_rec.append(len(board))

            if nstop == 2022:
                print(len(board))
            # print(nstop)
            # show(board)


period = npiece * nd
# print(period)

# this is a roundabout and unrigorous way of doing things but I'm not particularly motivated to improve this

full_ht = np.array(full_ht)
full_n = np.array(full_n)

fn_diff = full_n[1:] - full_n[:-1]
# print(fn_diff)
# print(np.argwhere(fn_diff == 53))

best_period = 0
min_var = 1e10

for p_try in range(1, len(full_n) // 3):
    fn_diff2 = full_n[p_try:] - full_n[:-p_try]
    this_var = np.var(fn_diff2)
    if this_var < min_var:
        min_var = this_var
        best_period = p_try
# print(fn_diff2[:5])
period2 = (full_n[best_period:] - full_n[:-best_period])[0]
# print(period, period2, np.lcm(period, period2))


ht_rec = np.array(ht_rec)
rem = 3*1740+1
rem = 1000000000000 % period2
test_vals = ht_rec[[rem, rem+period2, rem+period2*2, rem+period2*3, rem+period2*4]]
diff = test_vals[1:] - test_vals[:-1]
# print(diff)

n_period2s = (1000000000000 - rem) //period2
# print(n_period2s)
print(ht_rec[rem] + n_period2s * diff[0])
slope = diff[0] / period2

xvals = np.arange(1, len(ht_rec)+1)
yvals = ht_rec - xvals * slope
yvals2 = full_ht - full_n * slope
plt.plot(xvals, yvals, '-')
plt.plot(full_n, yvals2, '.', markersize=10)

# plt.plot(ht_rec[period2:] - ht_rec[:-period2], '.-')  # residuals of periodicity
plt.show()