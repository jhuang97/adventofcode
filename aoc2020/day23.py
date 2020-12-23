input = open('day_23_input.txt', 'r').read()
# input = '389125467'

nums = [int(k) for k in list(input)]

current = nums[0]

prev = dict()
later = dict()
for k in range(len(nums)):
	prev[nums[k]] = nums[(k-1) % len(nums)]
	later[nums[k]] = nums[(k+1) % len(nums)]

min_lbl = min(nums)
max_lbl = max(nums)


def make_moves(num_moves, current, prev, later, min_lbl, max_lbl):
	for t in range(num_moves):
		# if t % 100000 == 0:
		# 	print(t)
		cur_3 = current
		picked_up = []
		for _ in range(3):
			cur_3 = later[cur_3]
			picked_up.append(cur_3)
		cur_3 = later[cur_3]

		prev[cur_3] = current
		later[current] = cur_3

		dest = current-1
		if dest < min_lbl:
			dest = max_lbl
		while dest in picked_up:
			dest -= 1
			if dest < min_lbl:
				dest = max_lbl
		dest_later = later[dest]
		later[dest] = picked_up[0]
		prev[picked_up[0]] = dest
		later[picked_up[2]] = dest_later
		prev[dest_later] = picked_up[2]
		current = later[current]

make_moves(100, current, prev, later, min_lbl, max_lbl)

out = ''
elem = 1
for _ in range(8):
	elem = later[elem]
	out += str(elem)
print(out)


current = nums[0]
min_num = min(nums)
max_num = max(nums)
num_cups = 1000000

prev = dict()
later = dict()
for k in range(1, len(nums)):
	prev[nums[k]] = nums[k-1]
	later[nums[k-1]] = nums[k]
prev[nums[0]] = num_cups
later[num_cups] = nums[0]

prev[max_num+1] = nums[-1]
later[nums[-1]] = max_num+1
for k in range(max_num+2, num_cups+1):
	prev[k] = k-1
	later[k-1] = k

# print(current)
# for _ in range(num_cups):
# 	current = prev[current]
# print(current)
make_moves(10000000, current, prev, later, min_lbl, num_cups)
elem = 1
prod = 1
for _ in range(2):
	elem = later[elem]
	prod *= elem
print(prod)