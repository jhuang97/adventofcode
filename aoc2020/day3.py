file1 = open('day_3_input.txt', 'r')
lines = file1.read().splitlines()


def count_trees(lines, dx, dy):
    nchar = len(lines[0])
    n_trees = 0
    x = 0
    y = 0
    while y < len(lines):
        if lines[y][x % nchar] == '#':
            n_trees += 1
        x += dx
        y += dy

    return n_trees

prod = 1
slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
for dx, dy in slopes:
    prod *= count_trees(lines, dx, dy)

print(prod)