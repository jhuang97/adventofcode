file1 = open('day1_input.txt', 'r')
lines = file1.read().split('\n\n')

cals = [sum([int(s) for s in a.splitlines()]) for a in lines]
print(max(cals))

cals.sort()
print(sum(cals[-3:]))
