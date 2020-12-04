import re

file1 = open('day_4_input.txt', 'r')
passports = file1.read().split('\n\n')

fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
ofield = 'cid'


def good_yr(str, y1, y2):
    if len(str) == 4 and str.isnumeric():
        return y1 <= int(str) <= y2
    else:
        return False


def good_ht(str):
    if len(str) > 2:
        if str[:-2].isnumeric():
            if str[-2:] == 'cm':
                return 150 <= int(str[:-2]) <= 193
            elif str[-2:] == 'in':
                return 59 <= int(str[:-2]) <= 76
    return False


count = 0
allvalid_count = 0
for p in passports:
    valid = True
    for f in fields:
        if f not in p:
            valid = False
    if valid:
        count += 1
        tokens = p.split()
        allvalid = True
        for t in tokens:
            kv = t.split(':')
            key = kv[0]
            val = kv[1]
            try:
                fieldvalid = {
                    'byr': lambda v: good_yr(v, 1920, 2002),
                    'iyr': lambda v: good_yr(v, 2010, 2020),
                    'eyr': lambda v: good_yr(v, 2020, 2030),
                    'hgt': lambda v: good_ht(v),
                    'hcl': lambda v: re.fullmatch(r'\#[0-9|a-f]{6}', v) is not None,
                    'ecl': lambda v: v in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
                    'pid': lambda v: re.fullmatch(r'\d{9}', v) is not None,
                    'cid': lambda v: True
                }[key](val)
                if not fieldvalid:
                    allvalid = False
            except KeyError as e:
                allvalid = False
                print('oh no')
                print(t)

        if allvalid:
            allvalid_count += 1

print(count)
print(allvalid_count)