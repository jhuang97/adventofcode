file1 = open('day02_in.txt', 'r')

lines = file1.read().strip().split('\n')

idx = {'A': 0, 'B': 1, 'C': 2}
idx2 = {'X': 0, 'Y': 1, 'Z': 2}
pts = {'X':1, 'Y':2, 'Z':3}

total = 0
for l in lines:
	letters = l.split()
	total += pts[letters[1]]
	a, b = idx[letters[0]], idx2[letters[1]]
	if a == b:
		total += 3
	elif b-a == 1 or b-a == -2:
		total += 6
print(total)

total = 0
pts = {'A':1, 'B':2, 'C':3}
moves = ['A', 'B', 'C']
delta = {'X':-1, 'Y':0, 'Z':1}
game_pts = {'X':0, 'Y':3, 'Z':6}

for l in lines:
	letters = l.split()
	total += game_pts[letters[1]]
	my_move = idx[letters[0]] + delta[letters[1]]
	if my_move < 0:
		my_move += 3
	if my_move >= 3:
		my_move -= 3
	total += pts[moves[my_move]]
print(total)
