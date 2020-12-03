file1 = open('day_2_input.txt', 'r')
lines = file1.read().splitlines()

# count = 0
# for line in lines:
#     tokens = line.split(' ')
#     if len(tokens) == 3:
#         freqs = [int(k) for k in tokens[0].split('-')]
#         letter = tokens[1][:1]
#         mcount = tokens[2].count(letter)
#         if freqs[0] <= mcount and mcount <= freqs[1]:
#             count += 1

count = 0
for line in lines:
    tokens = line.split(' ')
    if len(tokens) == 3:
        freqs = [int(k) for k in tokens[0].split('-')]
        letter = tokens[1][:1]
        mcount = tokens[2].count(letter)
        if bool(tokens[2][freqs[0]-1] == letter) ^ bool(tokens[2][freqs[1]-1] == letter):
            count += 1

print(count)