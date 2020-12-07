file1 = open('day_6_input.txt', 'r')
decl_groups = file1.read().split('\n\n')

total = 0
total2 = 0
for d in decl_groups:
    decls = d.rstrip().split('\n')
    qs = set()
    intersect = set()
    for idx, d in enumerate(decls):
        for c in d:
            qs.add(c)
        if idx == 0:
            for c in d:
                intersect.add(c)
        else:
            new_set = set()
            for c in d:
                if c in intersect:
                    new_set.add(c)
            intersect = new_set
    total += len(qs)
    print(len(intersect))
    total2 += len(intersect)

print(total)
print(total2)