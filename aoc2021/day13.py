import numpy as np

file1 = open('day_13_input.txt', 'r')
lines = file1.read().strip().split('\n\n')
# lines = """6,10
# 0,14
# 9,10
# 0,3
# 10,4
# 4,11
# 6,0
# 6,12
# 4,1
# 0,13
# 10,12
# 3,4
# 3,0
# 8,4
# 1,10
# 2,14
# 8,10
# 9,0
#
# fold along y=7
# fold along x=5""".split('\n\n')
d_lines = lines[0].splitlines()
f_lines = lines[1].splitlines()

pts = []
for l in d_lines:
    sides = l.split(',')
    pts.append([int(sides[0]), int(sides[1])])
folds = []
for l in f_lines:
    sides = l[11:].split('=')
    folds.append([sides[0], int(sides[1])])

pts = np.array(pts)


def apply_fold(pts, fold):
    if fold[0] == 'y':
        f_dim = 1
    elif fold[0] == 'x':
        f_dim = 0

    fpos = fold[1]
    pts[:, f_dim] = pts[:, f_dim] * (pts[:, f_dim] < fpos) + (2*fpos - pts[:, f_dim])*(pts[:, f_dim] >= fpos)
    return pts


pts_new = apply_fold(pts, folds[0])
# print(np.shape(pts_new))
pts_new_unique = np.unique(pts_new, axis=0)
print(np.shape(pts_new_unique)[0])
# print(pts_new_unique)

for k in range(1, len(folds)):
    pts_new = apply_fold(pts_new, folds[k])


def show_pts(pts):
    arr = np.zeros(pts.max(axis=0)+1)
    for k in range(np.shape(pts)[0]):
        arr[pts[k, 0], pts[k, 1]] = 1
    arr = np.transpose(arr)
    for r in arr:
        str = ''
        for c in r:
            if c == 0:
                str += '   '
            else:
                str += '###'
        print(str)


show_pts(pts_new)