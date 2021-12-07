import numpy as np

file1 = open('day_6_input.txt', 'r')
lines = file1.read().strip().split(',')
# lines = '3,4,3,1,2'.split(',')

hist = np.zeros(9, dtype=int)
for s in lines:
    hist[int(s)] += 1


def update(vec):
    new_vec = np.zeros(9, dtype=int)
    for k in range(1, 9):
        new_vec[k-1] += vec[k]
    new_vec[6] += vec[0]
    new_vec[8] += vec[0]
    return new_vec


for _ in range(80):
    hist = update(hist)
print(np.sum(hist))

for _ in range(256-80):
    hist = update(hist)
print(np.sum(hist))
