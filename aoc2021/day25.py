import numpy as np

fname = 'day_25_input.txt'
# fname = 'day_25_test.txt'
file1 = open(fname, 'r')
lines = file1.read().strip().splitlines()

nr = len(lines)
nc = len(lines[0])

right = np.zeros((nr, nc), dtype=bool)
down = np.zeros((nr, nc), dtype=bool)

for iy in range(nr):
	for ix in range(nc):
		if lines[iy][ix] == '>':
			right[iy][ix] = True
		elif lines[iy][ix] == 'v':
			down[iy][ix] = True

k = 0
while True:
	# east
	occupied = np.roll(right | down, -1, axis=1)
	right_stay = right & occupied
	right_go = right & ~occupied
	right = right_stay | np.roll(right_go, 1, axis=1)

	# south
	occupied = np.roll(right | down, -1, axis=0)
	down_stay = down & occupied
	down_go = down & ~occupied
	down = down_stay | np.roll(down_go, 1, axis=0)
	
	k += 1
	if np.sum(right_go) + np.sum(down_go) == 0:
		print(k)
		break