import numpy as np
from collections import defaultdict

file = open('day23_in.txt', 'r')
# file = open('day23_test.txt', 'r')
lines = file.read().strip().splitlines()

nr_i = len(lines)
nc_i = len(lines[0])

pts = set()
for ir, l in enumerate(lines):
	for ic, c in enumerate(l):
		if c == '#':
			pts.add((ir, ic))

# print(nr_i, nc_i, len(pts))
# print(pts)

dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def get_bounds(pts):
	r_min, c_min = 100000000, 100000000
	r_max, c_max = -100000000, -100000000
	for r, c in pts:
		r_min = min(r, r_min)
		c_min = min(c, c_min)
		r_max = max(r, r_max)
		c_max = max(c, c_max)
	return r_min, r_max, c_min, c_max


def print_pts(pts):
	r_min, r_max, c_min, c_max = get_bounds(pts)

	board = np.zeros((r_max-r_min+1, c_max-c_min+1), dtype=int)
	for r, c in pts:
		board[r-r_min, c-c_min] = 1

	for row in board:
		for elem in row:
			print('#' if elem == 1 else '.', end='')
		print()


def has_neighbor(pt):
	r, c = pt
	for dr in [-1, 0, 1]:
		for dc in [-1, 0, 1]:
			if dr != 0 or dc != 0:
				if (r+dr, c+dc) in pts:
					return True
	return False


def can_move(r, c, mdir):
	dr, dc = mdir
	for ddr in ([dr] if dr != 0 else [-1, 0, 1]):
		for ddc in ([dc] if dc != 0 else [-1, 0, 1]):
			if (r + ddr, c + ddc) in pts:
				return False
	return True


def propose(p, dir_offset):
	r, c = p
	for k in range(4):
		d = dirs[(k + dir_offset) % 4]
		if can_move(r, c, d):
			return r + d[0], c + d[1]


dir_offset = 0
t = 1
while True:
	pts_propose = defaultdict(list)
	for p in pts:
		if has_neighbor(p):
			pt_prop = propose(p, dir_offset)
			if pt_prop is not None:
				pts_propose[pt_prop].append(p)

	no_move = True
	for dest, src_list in pts_propose.items():
		if len(src_list) == 1:
			pts.remove(src_list[0])
			pts.add(dest)
			no_move = False
	dir_offset = (dir_offset + 1) % 4

	if t == 10:
		r_min, r_max, c_min, c_max = get_bounds(pts)
		print((r_max-r_min+1) * (c_max-c_min+1) - len(pts))

	if no_move:
		print(t)
		break
	t += 1

	# print(f'after {k+1} rounds')
	# print_pts(pts)