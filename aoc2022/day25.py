import numpy as np

file = open('day25_in.txt', 'r')
lines = file.read().strip().splitlines()

# print(len(lines))
# print(max([len(n) for n in lines]))

nd = max([len(n) for n in lines])
digits = np.zeros(nd, dtype=int)
for l in lines:
	for pos, c in enumerate(l[::-1]):
		if c in '012':
			num = int(c)
		elif c == '-':
			num = -1
		elif c == '=':
			num = -2
		else:
			print('oh no')
		digits[pos] += num


for k in range(nd-1):
	mult = digits[k] // 5
	rem = digits[k] % 5
	if rem > 2:
		mult += 1
		rem -= 5
	digits[k] = rem
	digits[k+1] += mult
# print(digits)

for d in digits[::-1]:
	if 0 <= d <= 2:
		print(d, end='')
	elif d == -1:
		print('-', end='')
	elif d == -2:
		print('=', end='')
	else:
		print('oh no')