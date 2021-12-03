file1 = open('day_2_input.txt', 'r')
lines = file1.read().splitlines()

x = 0
depth = 0
for line in lines:
    tokens = line.split(' ')
    amt = int(tokens[1])
    if tokens[0] == 'forward':
        x += amt
    elif tokens[0] == 'down':
        depth += amt
    elif tokens[0] == 'up':
        depth -= amt

print(x*depth)

x = 0
depth = 0
aim = 0
for line in lines:
    tokens = line.split(' ')
    amt = int(tokens[1])
    if tokens[0] == 'forward':
        x += amt
        depth += aim*amt
    elif tokens[0] == 'down':
        aim += amt
    elif tokens[0] == 'up':
        aim -= amt
print(x*depth)