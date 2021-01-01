import numpy as np

file1 = open('day_24_input.txt', 'r')
addrs = file1.read().splitlines()

dirs = {'e':(1,0), 'ne':(0,1), 'nw': (-1, 1), 'w':(-1, 0), 'sw':(0, -1), 'se':(1, -1)}
tile_dirs = []

for a in addrs:
	idx = 0
	step_list = []
	while idx < len(a):
		if a[idx:idx+1] in dirs:
			step_list.append(a[idx:idx+1])
			idx += 1
		elif a[idx:idx+2] in dirs:
			step_list.append(a[idx:idx+2])
			idx += 2
		else:
			print('oh no')
	tile_dirs.append(step_list)

	# print(a)
	# print(step_list)

flipped = set()
for td in tile_dirs:
	ptr = np.array([0, 0])
	for step in td:
		ptr = ptr + np.array(dirs[step])
	if tuple(ptr) in flipped:
		flipped.remove(tuple(ptr))
	else:
		flipped.add(tuple(ptr))

print(len(flipped))



def neighbors(pt):
	out = []
	for d in dirs.values():
		out.append((pt[0] + d[0], pt[1] + d[1]))
	return out


for k in range(100):
	to_check = set()
	for pt in flipped:
		to_check.add(pt)
		for pt2 in neighbors(pt):
			to_check.add(pt2)
	
	next_flipped = set()
	for tile in to_check:
		num_neighbors = 0
		for pt2 in neighbors(tile):
			if pt2 in flipped:
				num_neighbors += 1 
		if tile in flipped:
			if num_neighbors == 1 or num_neighbors == 2: # black tiles with 1 neighbor survive
				next_flipped.add(tile)
		else:
			if num_neighbors == 2: # white tiles with 2 neighbors become black
				next_flipped.add(tile)
	flipped = next_flipped

print(len(flipped))