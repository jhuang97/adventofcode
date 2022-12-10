import numpy as np
import matplotlib.pyplot as plt

file1 = open('day08_in.txt', 'r')
lines = file1.read().strip().split('\n')
digits = np.array([[int(c) for c in l] for l in lines])
# print(digits.shape)
nr, nc = digits.shape

# top visible
vis_left = np.full(digits.shape, True)
tall = digits[:, 0]
for k in range(1, nc):
    vis_left[:, k] = digits[:, k] > tall
    tall = np.maximum(tall, digits[:, k])

vis_top = np.full(digits.shape, True)
tall = digits[0, :]
for k in range(1, nr):
    vis_top[k, :] = digits[k, :] > tall
    tall = np.maximum(tall, digits[k, :])

vis_right = np.full(digits.shape, True)
tall = digits[:, nc-1]
for k in range(nc-2, -1, -1):
    vis_right[:, k] = digits[:, k] > tall
    tall = np.maximum(tall, digits[:, k])

vis_bot = np.full(digits.shape, True)
tall = digits[nr-1, :]
for k in range(nr-2, -1, -1):
    vis_bot[k, :] = digits[k, :] > tall
    tall = np.maximum(tall, digits[k, :])

# plt.imshow(vis_bot)
# plt.show()
print(np.sum(vis_bot | vis_right | vis_top | vis_left))

best_so_far = 0
for r in range(nr):
    for c in range(nc):
        # print(r, c)
        prod = 1
        height = digits[r, c]
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            mr, mc = r, c
            dist = 0
            while True:
                mr += dr
                mc += dc
                if mr < 0 or mr >= nr or mc < 0 or mc >= nc:
                    break
                dist += 1
                if digits[mr, mc] >= height:
                    break
            prod *= dist
        if prod > best_so_far:
            best_so_far = prod
print(best_so_far)
