import numpy as np
file1 = open('day_16_input.txt', 'r')
sections = file1.read().split('\n\n')

reqs = []
field_names = []
for l in sections[0].split('\n'):
    s1 = l.split(': ')
    field_names.append(s1[0])
    this_req = []
    for s2 in s1[1].split(' or '):
        lims = [int(s3) for s3 in s2.split('-')]
        this_req.append(lims)
    reqs.append(this_req)

nearby_tickets = []
for l in sections[2].split('\n')[1:]:
    if len(l) > 0:
        nearby_tickets.append([int(n) for n in l.split(',')])


def invalid_vals(ticket, reqs):
    assert len(ticket) == len(reqs)
    total = 0
    allvalid = True
    for i in range(len(ticket)):
        valid = False
        for subreq in reqs:
            for lims in subreq:
                if lims[0] <= ticket[i] <= lims[1]:
                    valid = True
        if not valid:
            total += ticket[i]
            allvalid = False
            # print(ticket[i])
    return total, allvalid


total = 0
good_tickets = []
for ticket in nearby_tickets:
    rate, valid = invalid_vals(ticket, reqs)
    if valid:
        good_tickets.append(ticket)
    else:
        total += rate
print(total)


def is_consistent(tickets, reqs, fidx):
    for t in tickets:
        valid = False
        for lims in reqs:
            if lims[0] <= t[fidx] <= lims[1]:
                valid = True
        if not valid:
            return False
    return True


num_fields = len(good_tickets[0])
num_done = 0
fidx = 0
fidx_to_nidx = {}
consistency = np.zeros((num_fields, num_fields))  # fidx, nidx
for fidx in range(num_fields):
    for nidx in range(num_fields):
        consistency[fidx, nidx] = int(is_consistent(good_tickets, reqs[nidx], fidx))

naxis = 0
idx_done = [[], []]
while num_done < num_fields:
    deduce = np.where(consistency.sum(axis=naxis) == 1)[0]
    deduce = [i for i in deduce if i not in idx_done[1-naxis]]
    if len(deduce) > 0:
        if naxis == 0:
            nidx2 = deduce[0]
            deduce2 = np.where(consistency[:,nidx2] == 1)[0]
            deduce2 = [i for i in deduce2 if i not in idx_done[naxis]]
            fidx2 = deduce2[0]
        elif naxis == 1:
            fidx2 = deduce[0]
            deduce2 = np.where(consistency[fidx2, :] == 1)[0]
            deduce2 = [i for i in deduce2 if i not in idx_done[naxis]]
            nidx2 = deduce2[0]

        # print(idx_done)
        fidx_to_nidx[fidx2] = nidx2
        idx_done[0].append(fidx2)
        idx_done[1].append(nidx2)
        consistency[:, nidx2] = 0
        consistency[fidx2, :] = 0
        consistency[fidx2, nidx2] = 1
        num_done += 1

    naxis = 1-naxis

prod = 1
your_ticket = [int(i) for i in sections[1].splitlines()[1].split(',')]
for i in range(num_fields):
    if field_names[fidx_to_nidx[i]].startswith('departure'):
        prod *= your_ticket[i]
print(prod)