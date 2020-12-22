file1 = open('day_21_input.txt', 'r')
lines = file1.read().splitlines()

ingred_ls = []
allergen_ls = []
all_ingreds = set()
all_allergens = set()
for l in lines:
    parts = l.split(' (contains ')
    ingreds = parts[0].split()
    allergens = parts[1][:-1].split(', ')
    ingred_ls.append(ingreds)
    allergen_ls.append(allergens)
    for w in ingreds:
        all_ingreds.add(w)
    for w in allergens:
        all_allergens.add(w)

ingred_idx = dict()
allergen_idx = dict()
for i in all_ingreds:
    ingred_idx[i] = set()
for i in all_allergens:
    allergen_idx[i] = set()
for idx, alist in enumerate(ingred_ls):
    for w in alist:
        ingred_idx[w].add(idx)
for idx, alist in enumerate(allergen_ls):
    for w in alist:
        allergen_idx[w].add(idx)

sus_ingreds = dict()
for ingred, iidx in ingred_idx.items():
    for allergen, aidx in allergen_idx.items():
        if aidx.issubset(iidx):
            if ingred in sus_ingreds:
                sus_ingreds[ingred].add(allergen)
            else:
                sus_ingreds[ingred] = set()
                sus_ingreds[ingred].add(allergen)

num_appear = 0
for ingred, iidx in ingred_idx.items():
    if ingred not in sus_ingreds:
        num_appear += len(iidx)
print(num_appear)

ia_matches = []
while len(sus_ingreds) > 0:
    ingred_match = None
    allergen_match = None
    for ingred, pos_allergens in sus_ingreds.items():
        if len(pos_allergens) == 1:
            ingred_match = ingred
            allergen_match = pos_allergens.pop()
            break
    sus_ingreds.pop(ingred_match)
    ia_matches.append((ingred_match, allergen_match))
    for pos_allergens in sus_ingreds.values():
        pos_allergens.discard(allergen_match)

ia_matches.sort(key=lambda tup: tup[1])
out_str = ""
for i, a in ia_matches:
    out_str += i + ","
print(out_str[:-1])