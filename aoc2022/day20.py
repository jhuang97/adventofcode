import numpy as np

file = open('day20_in.txt', 'r')
num_str = file.read().strip().splitlines()
nums = np.array([int(n) for n in num_str])
# nums = np.array([1, 2, -3, 3, -2, 0, 4])

right = np.zeros(len(nums), dtype=int)
left = np.zeros(len(nums), dtype=int)

right[:-1] = np.arange(1, len(nums))
right[-1] = 0
left[1:] = np.arange(len(nums)-1)
left[0] = len(nums)-1


# assume that i2 is to the right of i1
def swap(i1, i2):
	right_i2 = right[i2]
	left_i1 = left[i1]

	right[left_i1], right[i2], right[i1] = i2, i1, right_i2
	left[i2], left[i1], left[right_i2] = left_i1, i2, i1



def move(idx, dist):
	from_left, from_right = left[idx], right[idx]
	if dist > 0:
		to_left = idx
		for _ in range(abs(dist)):
			to_left = right[to_left]
		to_right = right[to_left]
	elif dist < 0:
		to_right = idx
		for _ in range(abs(dist)):
			to_right = left[to_right]
		to_left = left[to_right]

	right[from_left], left[from_right] = from_right, from_left
	right[idx], left[idx] = to_right, to_left
	right[to_left], left[to_right] = idx, idx


def decrypt(nums, n_mix):
	# print(np.where(nums==0))
	idx_0 = np.where(nums == 0)[0][0]
	p = len(nums)-1
	phalf = p//2
	nums_modded = (nums + phalf) % p - phalf


	right[:-1] = np.arange(1, len(nums))
	right[-1] = 0
	left[1:] = np.arange(len(nums)-1)
	left[0] = len(nums)-1


	for mix_index in range(n_mix):
		print(mix_index)
		for k in range(len(nums)):
			# if k % 2000 == 0:
			# 	print(k)
			# nmove = np.abs(nums[k])
			# move_dist = nums[k]
			# move_dist = nums[k] % (len(nums) - 1)
			move_dist = nums_modded[k]
			if move_dist != 0:
				move(k, move_dist)

		# print(f'turn {k}')
		# print(k, nums[k], nums[k] % len(nums))

		# list_str = ''
		# idx = 0
		# for _ in range(len(nums)):
		# 	list_str += str(nums[idx]) + ' '
		# 	idx = right[idx]
		# print(list_str)

	grove_num = []
	idx = idx_0
	for _ in range(3):
		for _ in range(1000):
			idx = right[idx]
		grove_num.append(nums[idx])
	# print(grove_num)
	return sum(grove_num)


print(decrypt(np.array([int(n) for n in num_str]), 1))
print(decrypt(np.array([int(n) * 811589153 for n in num_str]), 10))