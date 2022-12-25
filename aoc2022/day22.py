import numpy as np
from numpy.linalg import matrix_power

file = open('day22_in.txt', 'r')
# file = open('day22_test.txt', 'r')
parts = file.read().rstrip().split('\n\n')

map_lines = parts[0].split('\n')
nr = len(map_lines)
nc = max([len(l) for l in map_lines])
# print(map_lines)
# print(nr, nc)

board = np.full((nr, nc), -2)
for ir, l in enumerate(map_lines):
	for ic, c in enumerate(l):
		if c == '.':
			board[ir][ic] = -1
		elif c == '#':
			board[ir][ic] = 4
board_backup = board.copy()


path_list = []
idx0 = None
idx = 0
while idx < len(parts[1]):
	if parts[1][idx].isnumeric():
		if idx0 is None:
			idx0 = idx
	elif parts[1][idx] in ['L', 'R']:
		if idx0 is not None:
			path_list.append(int(parts[1][idx0:idx]))
			idx0 = None
		path_list.append(parts[1][idx])
	else:
		print('oh no')
	idx += 1
if idx0 is not None:
	path_list.append(int(parts[1][idx0:idx]))
# print(path_list)



def print_board(board):
	nr, nc = np.shape(board)
	for ir in range(nr):
		for ic in range(nc):
			c = board[ir][ic]
			if c == -2:
				print(' ', end='')
			elif c == -1:
				print('.', end='')
			elif c == 0:
				print('>', end='')
			elif c == 1:
				print('v', end='')
			elif c == 2:
				print('<', end='')
			elif c == 3:
				print('^', end='')
			elif c == 4:
				print('#', end='')
		print('\n', end='')


# print(map_lines[0])


# 50-149, 50-99, 0-99, 0-49
 ##
 #
##
#

cmin = np.zeros((nr,), dtype=int)
cmax = np.zeros((nr,), dtype=int)
rmin = np.zeros((nc,), dtype=int)
rmax = np.zeros((nc,), dtype=int)

for ir in range(nr):
	r = np.where(board[ir] >= -1)
	# print(ir, np.min(r), np.max(r))
	cmin[ir], cmax[ir] = np.min(r), np.max(r)
for ic in range(nc):
	c = np.where(board[:, ic] >= -1)
	rmin[ic], rmax[ic] = np.min(c), np.max(c)


dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
# d_chars = ['>', 'v', '<', '^']
r, c = 0, cmin[0]
facing = 0

for p in path_list:
	if isinstance(p, int):
		for _ in range(p):
			dr, dc = dirs[facing]
			rnext, cnext = r + dr, c + dc
			# print('try', rnext, cnext, 'state', r, c, facing, dr, dc)
			if rnext > rmax[c]:
				rnext = rmin[c]
			if rnext < rmin[c]:
				rnext = rmax[c]
			if cnext > cmax[r]:
				cnext = cmin[r]
			if cnext < cmin[r]:
				cnext = cmax[r]

			if board[rnext, cnext] == 4:
				# print('wall at', rnext, cnext, 'state', r, c, facing)
				break
			elif board[rnext, cnext] == -2:
				print('oh no')
			else:
				r, c = rnext, cnext
				board[r, c] = facing
	elif p == 'R':
		facing = (facing + 1) % 4
		board[r, c] = facing
	elif p == 'L':
		facing = (facing - 1) % 4
		board[r, c] = facing
	else:
		print('oh no')

# print_board(board)

print(r, c, facing)
print(1000*(r+1) + 4*(c+1) + facing)


board = board_backup.copy()

tile_size = np.gcd.reduce(cmax + 1)
ntr, ntc = nr // tile_size, nc // tile_size
# print(tile_size, ntr, ntc)
tiles = []
for ir in range(ntr):
	for ic in range(ntc):
		if board[tile_size*ir, tile_size*ic] > -2:
			tiles.append((ir, ic))
# print(tiles)

# setting up separate 3D coordinate system
Rz = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]], dtype=int)
Ry = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]], dtype=int)
Rx = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]], dtype=int)

R_tile = {}
R_tile[(1,0)] = Rx # DOWN
R_tile[(-1,0)] = matrix_power(Rx, 3) # UP
R_tile[(0,1)] = Ry # RIGHT
R_tile[(0,-1)] = matrix_power(Ry, 3) # LEFT

# y
# ^
# |
#  -> x

# initial face on +z side of cube
fidx = tiles.pop(0)
face = np.array([[1,1,1], [1,-1,1], [-1,-1,1], [-1,1,1]]).T  # [0,0,1]
f_tf = np.eye(3, dtype=int)
# print(face)
face_info = {fidx: (face, f_tf)}


def try_add_face():
	for irnew, icnew in tiles:
		for ir0, ic0 in face_info:
			dr = irnew - ir0
			dc = icnew - ic0
			if abs(dr) + abs(dc) == 1:
				fidxnew = (irnew, icnew)
				fold = face_info[(ir0, ic0)]
				tf_new = fold[1] @ R_tile[(dr, dc)]
				face_info[fidxnew] = (tf_new @ face, tf_new)
				added = True
				tiles.remove(fidxnew)
				# print((ir0, ic0), fidxnew, (dr, dc))
				# print(face_info[fidxnew][0])
				return


while tiles:
	try_add_face()
# print(face_info)


edge_map = {}


def try_match_edge(f1, f2):
	for k1 in range(4):
		v11 = face_info[f1][0][:, k1]
		v12 = face_info[f1][0][:, (k1 + 1) % 4]
		for k2 in range(4):
			v21 = face_info[f2][0][:, k2]
			v22 = face_info[f2][0][:, (k2 + 1) % 4]
			if np.all(v11 == v21) and np.all(v12 == v22):
				print('match', f1, f2, k1, k2, 'not supposed to happen')
				return
			if np.all(v11 == v22) and np.all(v12 == v21):
				# print('mirrored', f1, f2, k1, k2)
				edge_map[(f1, k1)] = (f2, k2)
				return


for face in face_info.keys():
	for face2 in face_info.keys():
		if face != face2:
			try_match_edge(face, face2)


# print(edge_map)


def offset_to_epos(offset, facing):
	r, c = offset
	if facing == 0:
		return r
	if facing == 1:
		return tile_size-1 - c
	if facing == 2:
		return tile_size-1 - r
	if facing == 3:
		return c


def epos_to_offset(epos, facing):
	t = tile_size-1
	if facing == 0:
		return epos, t
	if facing == 1:
		return t, t-epos
	if facing == 2:
		return t-epos, 0
	if facing == 3:
		return 0, epos


def wrap_3D(r, c, facing):
	offset = r % tile_size, c % tile_size
	epos = offset_to_epos(offset, facing)
	(tr_next, tc_next), edge_dest = edge_map[((r//tile_size, c//tile_size), facing)]
	off_r, off_c = epos_to_offset(tile_size-1 - epos, edge_dest)
	return tr_next*tile_size + off_r, tc_next*tile_size + off_c, (edge_dest + 2) % 4


r, c = 0, cmin[0]
facing = 0

for p in path_list:
	if isinstance(p, int):
		for _ in range(p):
			dr, dc = dirs[facing]
			rnext, cnext = r + dr, c + dc
			# print('try', rnext, cnext, 'state', r, c, facing, dr, dc)
			if rnext > rmax[c] or rnext < rmin[c] or cnext > cmax[r] or cnext < cmin[r]:
				rnext, cnext, fnext = wrap_3D(r, c, facing)
			else:
				fnext = facing

			if board[rnext, cnext] == 4:
				# print('wall at', rnext, cnext, 'state', r, c, facing)
				break
			elif board[rnext, cnext] == -2:
				print('oh no')
			else:
				r, c, facing = rnext, cnext, fnext
				board[r, c] = facing
	elif p == 'R':
		facing = (facing + 1) % 4
		board[r, c] = facing
	elif p == 'L':
		facing = (facing - 1) % 4
		board[r, c] = facing
	else:
		print('oh no')

# print_board(board)

print(r, c, facing)
print(1000*(r+1) + 4*(c+1) + facing)

# to continue rotation in the frame of the rotated face itself, matrix multiply the new rotation matrix on the right side
# tf1 = R_DOWN @ R_LEFT @ R_LEFT
# print(tf1 @ face)
# print(tf1 @ R_UP @ face)
# print(R_UP @ tf1 @ face)