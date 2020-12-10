import numpy as np

file1 = open('day_10_input.txt', 'r')
nums = np.array([int(n) for n in file1.read().splitlines()])
nums.sort()

count1 = 1
count3 = 1
for i in range(len(nums)-1):
    if nums[i+1]-nums[i] == 1:
        count1 += 1
    elif nums[i+1]-nums[i] == 3:
        count3 += 1

print(count1*count3)


def m(memo, max_jolt, n_ways):
    memo[max_jolt] = n_ways
    return n_ways


def num_ways(adapters, max_jolt, memo):
    if max_jolt in memo:
        return memo[max_jolt]
    if max_jolt == 0:
        return m(memo, max_jolt, 1)
    if max_jolt not in adapters and max_jolt != max(adapters)+3:
        return m(memo, max_jolt, 0)
    tot = 0
    for i in range(1, 4):
        # print(i)
        tot += num_ways(adapters, max_jolt-i, memo)
    return m(memo, max_jolt, tot)


memo = {}
print(num_ways(nums, max(nums)+3, memo))
# print(memo)
