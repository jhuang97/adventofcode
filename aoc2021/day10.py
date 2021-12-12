import numpy as np

file1 = open('day_10_input.txt', 'r')
lines = file1.read().strip().split('\n')

open_ch = ['(', '[', '{', '<']
close_ch = [')', ']', '}', '>']
match = {}
for k in range(4):
    match[open_ch[k]] = close_ch[k]
    match[close_ch[k]] = open_ch[k]

scores = {')':3, ']':57, '}':1197, '>':25137}


def error_score(l):
    mem = []
    for c in list(l):
        if c in open_ch:
            mem.append(c)
        else:
            if match[c] != mem.pop():
                return scores[c]
    return 0


incomplete = []
total = 0
for l in lines:
    score = error_score(l)
    total += score
    if score == 0:
        incomplete.append(l)
print(total)

cscores = {')':1, ']':2, '}':3, '>':4}


def auto_score(l):
    mem = []
    for c in list(l):
        if c in open_ch:
            mem.append(c)
        else:
            if match[c] != mem.pop():
                print('oh no')
    score = 0
    for c in reversed(mem):
        score *= 5
        score += cscores[match[c]]
    return score


auto_scores = [auto_score(l) for l in incomplete]
print(np.median(np.array(auto_scores)))
