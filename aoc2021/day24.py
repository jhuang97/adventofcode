from itertools import product

fname = 'day_24_input.txt'

file1 = open(fname, 'r')
sections = file1.read().strip().split('inp w\n')
sections = sections[1:]

num_sections = len(sections)
sections = [s.strip().splitlines() for s in sections]
num_lines = len(sections[0])
print(num_sections)

do_divide_arr = []
c1_arr = []
c2_arr = []
for k in range(num_sections):
	do_divide_arr.append(sections[k][3].split()[2] == '26')
	c1_arr.append(int(sections[k][4].split()[2]))
	c2_arr.append(int(sections[k][14].split()[2]))
# print(do_divide_arr)
# print(c1_arr)
# print(c2_arr)


# for k in range(num_lines):
# 	all_same = True
# 	print(k)
# 	for s in sections:
# 		if s[k] != sections[0][k]:
# 			all_same = False
# 			break
# 	if all_same:
# 		print(sections[0][k])
# 	else:
# 		for s in sections:
# 			print(s[k])


def base_list(n, b):
	out = []
	assert(n>=0)
	while n > 0:
		out.insert(0, n%b)
		n //= b
	return out


def update(state, w, c1, do_divide, c2):
	x, y, z = state
	x = (z % 26) + c1

	print('z', z, '=', base_list(z, 26), 'c1' , c1, 'x', x , ' z-> ' + str(int(z/26)) if do_divide else '', 'x', x, 'w', w, '(' if x == w else '', c2)

	if do_divide:
		z = int(z/26)

	if x != w:
		z *= 26
		z += w + c2

	return x, y, z


def run(w_arr, c1_arr, do_divide_arr, c2_arr):
	state = (0, 0, 0)
	for k in range(len(w_arr)):
		state = update(state, w_arr[k], c1_arr[k], do_divide_arr[k], c2_arr[k])
	x, y, z = state
	return z


# num_digit_check = 6
# for digits in product(range(1, 10), repeat=num_digit_check):
# 	z = run([9]*(num_sections-num_digit_check) + list(digits), c1_arr, do_divide_arr, c2_arr)
# 	if z == 0:
# 		print(num_digit_check)


# print(run([9]*(num_sections-3) + [8, 6, 1], c1_arr, do_divide_arr, c2_arr))
# test = [9,1,2,1,1,7,9,1,1,1,1,3,6,5]
# test = [3,1,2,1,1,7,9,1,1,1,1,3,6,7]
test = [5,1,9,8,3,9,9,9,9,4,7,9,9,9]  # part 1, by much guess and check
test = [1,1,2,1,1,7,9,1,1,1,1,3,6,5]  # part 2, by less guess and check
test_full = test + [1] * (num_sections - len(test))
print(run(test_full, c1_arr, do_divide_arr, c2_arr))
print(''.join([str(d) for d in test_full]))