import re
import matplotlib.pyplot as plt
import numpy as np


file1 = open('day15_in.txt', 'r')
yreport = 2000000
search_max = 4000000
# file1 = open('day15_test.txt', 'r')
# yreport = 10
# search_max = 20
lines = file1.read().strip().splitlines()


def manhattan(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])


sx = []
sy = []
bx = []
by = []
for l in lines:
    ss = [int(s) for s in re.findall(r'[-\d]+', l)]
    sx.append(ss[0])
    sy.append(ss[1])
    bx.append(ss[2])
    by.append(ss[3])


intervals = []
radii = []
for msx, msy, mbx, mby in zip(sx, sy, bx, by):
    mdist = manhattan((msx, msy), (mbx, mby))
    radii.append(mdist)
    dy = abs(msy-yreport)
    if dy <= mdist:
        dx_max = mdist - dy
        intervals.append((msx-dx_max, msx+dx_max))


def try_join(i1, i2):
    a1, a2 = i1
    b1, b2 = i2
    if (a1 <= b1 <= a2) or a2 + 1 == b1 or (b1 <= a1 <= b2) or b2 + 1 == a1:
        return min(a1, b1), max(a2, b2)


def join_all(intvs):
    indices = list(range(len(intvs)))
    out = []
    while len(indices) > 0:
        m_idx = indices.pop()
        m_intv = intvs[m_idx]
        while True:
            changed = False
            to_remove = []
            for idx in indices:
                join_res = try_join(m_intv, intvs[idx])
                if join_res is not None:
                    # print('joined', m_intv, intvs[idx], join_res)
                    m_intv = join_res
                    to_remove.append(idx)
                    changed = True
            for idx in to_remove:
                indices.remove(idx)
            if not changed:
                break
        out.append(m_intv)
        # s = ''
        # for idx in indices:
        #     s += str(intvs[idx])
        # print(out, s)
    return out


joined_intvs = join_all(intervals)
# print(intervals, joined_intvs)
tot_length = sum([a2-a1+1 for a1, a2 in joined_intvs])
# print(tot_length)
beacons = set(zip(bx, by))
for mbx, mby in beacons:
    if mby == yreport:
        within = False
        for a1, a2 in joined_intvs:
            if a1 <= mbx <= a2:
                within = True
        if within:
            tot_length -= 1
print(tot_length)


segments = []
for msx, msy, r in zip(sx, sy, radii):
    x1, x2 = msx-r, msx+r
    y1, y2 = msy-r, msy+r
    p1 = (x2, msy)
    p2 = (msx, y2)
    p3 = (x1, msy)
    p4 = (msx, y1)
    segments.append((p3, p4, -1))
    segments.append((p4, p1, 1))
    segments.append((p2, p1, -1))
    segments.append((p3, p2, 1))


fig, ax = plt.subplots()
for (x1, y1), (x2, y2), slope in segments:
    plt.plot([x1, x2], [y1, y2])


margin = 2


def crosses_box(sg, bounds):
    bx1, bx2, by1, by2 = bounds
    bx1 -= margin
    bx2 += margin
    by1 -= margin
    by2 += margin
    (x1, y1), (x2, y2), slope = sg # x1 < x2 but y1,y2 order not certain
    ymin, ymax = min(y1, y2), max(y1, y2)
    if (bx1 <= x1 <= bx2) or (x1 <= bx1 <= x2):
        # if (by1 <= ymin <= by2) or (ymin <= by1 <= ymax):
            xmin = max(x1, bx1)
            xmax = min(x2, bx2)
            ys1 = slope*(xmin-x1) + y1
            ys2 = slope*(xmax-x1) + y1

            if ys2 < ys1:
                ys1, ys2 = ys2, ys1
            if ys2 < by1 or by2 < ys1:
                # print(bounds, xmin, xmax, ys1, ys2)
                return False
            else:
                return True

    return False


THRESHOLD = 10000


def find_4_perim(bounds):
    n_crossing = 0
    for sg in segments:
        if crosses_box(sg, bounds):
            n_crossing += 1
        if n_crossing >= 4:
            break
    bx1, bx2, by1, by2 = bounds
    if n_crossing >= 4:
        if (bx2-bx1+1) * (by2-by1+1) >= THRESHOLD:
            # print('large', (bx2-bx1+1) * (by2-by1+1), bounds)
            xmid = (bx1 + bx2) // 2
            ymid = (by1 + by2) // 2
            find_4_perim((bx1, xmid, by1, ymid))
            find_4_perim((xmid+1, bx2, by1, ymid))
            find_4_perim((bx1, xmid, ymid+1, by2))
            find_4_perim((xmid+1, bx2, ymid+1, by2))
        else:
            # print(bounds)
            xvec = np.arange(bx1, bx2+1)
            yvec = np.arange(by1, by2+1)
            xv, yv = np.meshgrid(xvec, yvec)
            xv = np.reshape(xv, -1)
            yv = np.reshape(yv, -1)
            outside = np.ones(xv.shape, dtype=bool)
            for msx, msy, r in zip(sx, sy, radii):
                outside &= (np.absolute(xv - msx) + np.absolute(yv - msy)) > r
            if np.any(outside):
                idx = np.argwhere(outside)
                xans = xv[idx][0][0]
                yans = yv[idx][0][0]
                print(xans, yans)
                print(xans * search_max + yans)


find_4_perim((0, search_max, 0, search_max))
plt.show()

# 2900205 3139120

# mdists = []
# for msx, msy, mbx, mby in zip(sx, sy, bx, by):
#     mdists.append(manhattan((msx, msy), (mbx, mby)))
#
# for ycheck in range(search_max+1):
#     if ycheck % 100000 == 0:
#         print(ycheck)
#     intervals = []
#     for msx, msy, mbx, mby, mdist in zip(sx, sy, bx, by, mdists):
#         dy = abs(msy - ycheck)
#         if dy <= mdist:
#             dx_max = mdist - dy
#             intervals.append((msx - dx_max, msx + dx_max))
#     ji = join_all(intervals)
#     if len(ji) > 1:
#         vals = []
#         for v in [ji[0][0], ji[0][1], ji[1][0], ji[1][1]]:
#             if 0 <= v <= search_max:
#                 vals.append(v)
#         # print(vals, ycheck)
#         xb = min(vals)+1
#         print(xb, ycheck)
#         print(xb * search_max + ycheck)
#         break