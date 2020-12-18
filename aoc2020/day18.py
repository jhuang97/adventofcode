file1 = open('day_18_input.txt', 'r')
# file1 = open('day_17_test.txt', 'r')
lines = file1.read().splitlines()
ops = ['*', '+']

def tokenize(math):
    tokens = math.split()
    tokens2 = []
    for t in tokens:
        if t.isdigit() or t in ops:
            tokens2.append(t)
        else:
            ongoing_num = False
            num_str = ''
            for c in list(t):
                if c == '(' or c == ')':
                    if ongoing_num:
                        ongoing_num = False
                        if len(num_str) > 0:
                            tokens2.append(num_str)
                    tokens2.append(c)
                else:
                    assert c.isdigit()
                    if ongoing_num:
                        num_str += c
                    else:
                        ongoing_num = True
                        num_str = c
            if ongoing_num and len(num_str) > 0:
                tokens2.append(num_str)
    assert len(''.join(tokens2)) == len(''.join(tokens))
    return tokens2


def apply(val, op, val2):
    if op == '+':
        return val + val2
    elif op == '*':
        return val * val2


def eval_str(tokens):
    ctr = 0
    val = None
    op = None
    while ctr < len(tokens):
        t = tokens[ctr]
        if t.isdigit():
            if val is None:
                val = int(t)
            elif val is not None and op is not None:
                val = apply(val, op, int(t))
                op = None
            else:
                print('oh no')
            ctr += 1
        elif t in ops:
            op = t
            ctr += 1
        elif t == '(':
            pcount = 1
            ctr2 = ctr + 1
            while pcount > 0:
                if tokens[ctr2] == '(':
                    pcount += 1
                elif tokens[ctr2] == ')':
                    pcount -= 1
                ctr2 += 1
            # print(ctr2)
            pout = eval_str(tokens[ctr+1:ctr2-1])
            if val is None:
                val = pout
            elif val is not None and op is not None:
                val = apply(val, op, pout)
                op = None
            else:
                print('oh no')
            ctr = ctr2
    return val

total = 0
for l in lines:
    total += eval_str(tokenize(l))
print(total)

# print(eval_str(tokenize('1 + (2 * 3) + (4 * (5 + 6))')))


def eval_str2(tokens):
    times_idx = []
    pcount = 0
    for i, t in enumerate(tokens):
        if t == '(':
            pcount += 1
        elif t == ')':
            pcount -= 1
        elif t == '*':
            if pcount == 0:
                times_idx.append(i)

    times_idx.append(len(tokens))
    prev = -1
    sublists = []
    for i in times_idx:
        sublists.append(tokens[prev+1:i])
        prev = i

    # print(sublists)
    # process each sublist from left to right
    prod = 1
    for sl in sublists:
        ctr = 0
        val = None
        op = None
        while ctr < len(sl):
            t = sl[ctr]
            if t.isdigit():
                if val is None:
                    val = int(t)
                elif val is not None and op is not None:
                    val = apply(val, op, int(t))
                    op = None
                else:
                    print('oh no')
                ctr += 1
            elif t == '+':
                op = t
                ctr += 1
            elif t == '*':
                print('oh no')
            elif t == '(':
                pcount = 1
                ctr2 = ctr + 1
                while pcount > 0:
                    if sl[ctr2] == '(':
                        pcount += 1
                    elif sl[ctr2] == ')':
                        pcount -= 1
                    ctr2 += 1
                # print(ctr2)
                pout = eval_str2(sl[ctr + 1:ctr2 - 1])
                if val is None:
                    val = pout
                elif val is not None and op is not None:
                    val = apply(val, op, pout)
                    op = None
                else:
                    print('oh no')
                ctr = ctr2
        prod *= val
    return prod


total = 0
for l in lines:
    total += eval_str2(tokenize(l))
print(total)