import numpy as np

file1 = open('day_12_input.txt', 'r')
lines = file1.read().splitlines()

cardinal = {'N': np.array([0, 1]), 'E': np.array([1, 0]), 'S': np.array([0, -1]), 'W': np.array([-1, 0])}
card_arr = ['E', 'N', 'W', 'S']

pos = np.array([0,0])
facing = 0
for l in lines:
    letter = l[0]
    amt = int(l[1:])
    if letter in cardinal:
        pos = pos + amt * cardinal[letter]
    elif letter == 'L':
        n_turns = amt//90
        facing = (facing + n_turns) % 4
    elif letter == 'R':
        n_turns = amt//90
        facing = (facing - n_turns) % 4
    elif letter == 'F':
        pos = pos + amt * cardinal[card_arr[facing]]

print(np.sum(np.abs(pos)))

wayp = np.array([10, 1])
pos = np.array([0, 0])
for l in lines:
    letter = l[0]
    amt = int(l[1:])
    if letter in cardinal:
        wayp = wayp + amt * cardinal[letter]
    elif letter == 'L':
        n_turns = amt//90
        for k in range(n_turns):
            wayp = np.array([-wayp[1], wayp[0]])
    elif letter == 'R':
        n_turns = amt//90
        for k in range(n_turns):
            wayp = np.array([wayp[1], -wayp[0]])
    elif letter == 'F':
        pos = pos + amt * wayp
print(np.sum(np.abs(pos)))
