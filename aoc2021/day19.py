from collections import Counter
import numpy as np
from numpy.linalg import matrix_power

fname = 'day_19_input.txt'
# fname = 'day_19_test.txt'
file1 = open(fname, 'r')
sections = file1.read().strip().split('\n\n')

scans = []
for section in sections:
    lines = section.splitlines()
    arr = np.zeros((3, len(lines)-1), dtype=int)
    for k in range(1, len(lines)):
        tokens = lines[k].split(',')
        for r in range(3):
            arr[r, k-1] = int(tokens[r])
    scans.append(np.array(arr, dtype=int))

diffs_double = []
for scan in scans:
    num_vec = np.shape(scan)[1]
    arr2 = np.zeros((3, num_vec * (num_vec - 1)), dtype=int)
    idx = 0
    for k in range(num_vec-1):
        for m in range(k+1, num_vec):
            arr2[:, 2*idx] = scan[:, k] - scan[:, m]
            arr2[:, 2 * idx+1] = scan[:, m] - scan[:, k]
            idx += 1
    diffs_double.append(np.array(arr2).transpose())


Rz = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]], dtype=int)
Ry = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]], dtype=int)
Rx = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]], dtype=int)

rot_matrices = []
for yaw in range(4, 0, -1):
    for roll in range(4, 0, -1):
        rot_matrices.append(np.dot(matrix_power(Rz, yaw), matrix_power(Rx, roll)))
for pitch in [1, 3]:
    for roll in range(4, 0, -1):
        rot_matrices.append(np.dot(matrix_power(Ry, pitch), matrix_power(Rx, roll)))


diffs_rot = {}
for idx, scan in enumerate(scans):
    # print(idx)
    for rot_idx, rot_mat in enumerate(rot_matrices):
        coord_rot = np.dot(diffs_double[idx], rot_mat)
        rows = set()
        for row in coord_rot:
            rows.add(tuple(row))
        diffs_rot[(idx, rot_idx)] = rows
# print(diffs_rot)


n_scans = len(scans)
rot_mat_idx = [0] + (n_scans-1)*[None]
known_idx = [0]
known_diff = [diffs_double]
unknown_idx = list(range(1, n_scans))
threshold = 130
# threshold = 10
share_beacon_idx = []
while unknown_idx:
    found = False
    for k in unknown_idx:
        for idx, rot_mat in enumerate(rot_matrices):
            diff_rot = diffs_rot[(k, idx)]
            for m in known_idx:
                known_rot = diffs_rot[(m, rot_mat_idx[m])]
                count = 0
                for tup in diff_rot:
                    if tup in known_rot:
                        count += 1
                if count > threshold:
                    found = True
                    rot_mat_idx[k] = idx
                    known_idx.append(k)
                    unknown_idx.remove(k)
                    share_beacon_idx.append((m, k))
                    print(k, m, idx)
                    break
            if found:
                break
        if found:
            break
# print(rot_mat_idx)
# print(share_beacon_idx)

# figure out absolute coordinates
new_scans = []
for k in range(n_scans):
    new_scans.append(np.dot(scans[k].transpose(), rot_matrices[rot_mat_idx[k]]).transpose())

abs_coords = [scans[0]] + (n_scans-1)*[None]
shifts = [np.array([0, 0, 0])]
for i1, i2 in share_beacon_idx:
    c = Counter()
    num_vec1 = np.shape(scans[i1])[1]
    num_vec2 = np.shape(scans[i2])[1]
    for iv11 in range(num_vec1-1):
        v11 = abs_coords[i1][:, iv11]
        for iv12 in range(iv11+1, num_vec1):
            disp = abs_coords[i1][:, iv12] - v11
            for iv21 in range(num_vec2 - 1):
                v21 = new_scans[i2][:, iv21]
                for iv22 in range(iv21+1, num_vec2):
                    disp2 = new_scans[i2][:, iv22] - v21
                    if np.all(disp2 == disp):
                        c[tuple(v11-v21)] += 1
    # print(c.most_common(1))
    tup = c.most_common(1)[0][0]
    shift = np.array(list(tup))
    shifts.append(shift)
    abs_coords[i2] = new_scans[i2] + shift[:, None]


all_coords = np.unique(np.concatenate(abs_coords, axis=1), axis=1)
print(np.shape(all_coords)[1])
# print(shifts)

max_dist = -1
for k in range(len(shifts)-1):
    for m in range(k+1, len(shifts)):
        dist = np.sum(np.abs(shifts[k] - shifts[m]))
        if dist > max_dist:
            max_dist = dist
print(max_dist)
