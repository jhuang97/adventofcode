import re
file1 = open('day_7_input.txt', 'r')
lines = file1.read().splitlines()


def count_hold(ruleset, color):
    memo = {}
    bag_count = 0
    return count_hold_helper(ruleset, color, memo)-1


def count_hold_helper(ruleset, color, memo):
    if color in memo.keys():
        return memo[color]
    if len(ruleset[color]) == 0:
        memo[color] = 1
        return 1
    bag_count = 1
    for sub_color, sub_num in ruleset[color].items():
        bag_count += sub_num * count_hold_helper(ruleset, sub_color, memo)
    memo[color] = bag_count
    return bag_count


def can_hold(ruleset, color):
    memo = {}
    count = 0
    for r_color in ruleset.keys():
        if can_hold_helper(ruleset, r_color, color, memo):
            count += 1
    return count


def can_hold_helper(ruleset, holder, held, memo):
    if holder in memo.keys():
        return memo[holder]
    if len(ruleset[holder]) == 0:
        memo[holder] = False
        return False
    if held in ruleset[holder].keys():
        memo[holder] = True
        return True
    for r_color in ruleset[holder].keys():
        if can_hold_helper(ruleset, r_color, held, memo):
            memo[holder] = True
            return True
    memo[holder] = False
    return False


rules = {}
for l in lines:
    tokens = l.split(' contain ')
    m = re.search(r'.*(?=\sbag)', tokens[0])
    r_color = m.group(0)
    # print('color: ' + r_color)
    bag_list = {}
    for s in tokens[1].split(', '):
        if not s.startswith('no other'):
            m = re.match(r'(\d+) ([\w\s]+) bag', s)
            bag_list[m.group(2)] = int(m.group(1))
    rules[r_color] = bag_list

# print(rules)
print(can_hold(rules, 'shiny gold'))
print(count_hold(rules, 'shiny gold'))