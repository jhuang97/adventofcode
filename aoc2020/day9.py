import numpy as np

file1 = open('day_9_input.txt', 'r')
nums = np.array([int(n) for n in file1.read().splitlines()])
# print(nums)

preamble_len = 25
target = -1
for i in range(preamble_len, len(nums)):
    past = nums[i-preamble_len:i]
    can_add = False
    for j in range(preamble_len-1):
        for k in range(j+1, preamble_len):
            if past[j] + past[k] == nums[i]:
                can_add = True
                break
        if can_add:
            break

    if not can_add:
        print(nums[i])
        target = nums[i]
        break

cumu = nums.cumsum()
for i in range(preamble_len-1, len(nums)-2):
    for j in range(i+2, len(nums)):
        if cumu[j] - cumu[i] == target:
            contig = nums[i+1:j+1]
            print(min(contig) + max(contig))