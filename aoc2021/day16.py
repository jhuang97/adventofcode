file1 = open('day_16_input.txt', 'r')
line = file1.read().strip()
# line = "9C0141080250320F1802104A08"
b_str = ''.join(["{0:04b}".format(int(c, 16)) for c in list(line)])
# print(b_str)


def parse_p1(bstr):
    idx = 0
    expect = 'version'
    literal_str = ''
    version_total = 0
    packet_indices = [0]
    e_len = {'version': 3, 'typeID': 3, 'literal':5, 'l_typeID':1, 'nbits15':15, 'npackets11':11}
    while idx < len(bstr) - e_len[expect]:
        if expect == 'version':
            version = int(bstr[idx:idx+3], 2)
            version_total += version
            idx += 3
            expect = 'typeID'
        elif expect == 'typeID':
            typeID = int(bstr[idx:idx + 3], 2)
            idx += 3
            if typeID == 4:
                expect = 'literal'
            else:
                expect = 'l_typeID'
        elif expect == 'literal':
            lflag = bstr[idx]
            lpiece = bstr[idx+1:idx+5]
            idx += 5
            literal_str += lpiece
            if lflag == '0':
                literal_str = ''
                expect = 'version'
                packet_indices.append(idx)
        elif expect == 'l_typeID':
            l_typeID = bstr[idx]
            idx += 1
            if l_typeID == '0':
                expect = 'nbits15'
            elif l_typeID == '1':
                expect = 'npackets11'
        elif expect == 'nbits15':
            # nbits = int(bstr[idx:idx+15], 2)
            idx += 15
            expect = 'version'
            packet_indices.append(idx)
        elif expect == 'npackets11':
            # npackets = int(bstr[idx:idx+11], 2)
            idx += 11
            expect = 'version'
            packet_indices.append(idx)
    return version_total, packet_indices


v_total, pindices = parse_p1(b_str)
print(v_total)
pindices += [len(b_str)]
packets = [b_str[pindices[k]:pindices[k+1]] for k in range(len(pindices)-1)]
# print(packets)


def prod(l):
    out = 1
    for val in l:
        out *= val
    return out


def gt(l):
    return 1 if l[0] > l[1] else 0


def lt(l):
    return 1 if l[0] < l[1] else 0


def eq(l):
    return 1 if l[0] == l[1] else 0


def get_packet_value_v2(packets, pidx):
    p = packets[pidx]
    # print('pkt', pidx, p)
    typeID = int(p[3:6], 2)
    operators = [sum, prod, min, max, None, gt, lt, eq]

    if typeID == 4:
        idx = 6
        l_str = ''
        while True:
            lflag = p[idx]
            l_str += p[idx+1:idx+5]
            idx += 5
            if lflag == '0':
                val = int(l_str, 2)
                # print('literal', val)
                return val, pidx+1
    else:
        l_typeID = p[6]
        sub_vals = []
        pidx_sub = pidx + 1
        if l_typeID == '0':  # bits 15
            nbits = int(p[7:7 + 15], 2)
            bits_so_far = 0
            while bits_so_far < nbits:
                val, pidx_sub = get_packet_value_v2(packets, pidx_sub)
                sub_vals.append(val)
                bits_so_far = 0
                for k in range(pidx+1, pidx_sub):
                    bits_so_far += len(packets[k])
                # print('nbit sub get ', pidx_sub, bits_so_far, nbits)
        elif l_typeID == '1':  # packets 11
            npackets = int(p[7:7 + 11], 2)
            for k in range(npackets):
                val, pidx_sub = get_packet_value_v2(packets, pidx_sub)
                sub_vals.append(val)
        # print('op', typeID, sub_vals)
        return operators[typeID](sub_vals), pidx_sub


print(get_packet_value_v2(packets, 0)[0])


# def get_packet_value(bstr):
#     idx = 0
#     expect = 'version'
#     literal_str = ''
#     version_total = 0
#     operators = [sum, prod, min, max, None, gt, lt, eq]
#     e_len = {'version': 3, 'typeID': 3, 'literal': 5, 'l_typeID': 1, 'nbits15': 15, 'npackets11': 11}
#     while idx <= len(bstr) - e_len[expect]:
#         if expect == 'version':
#             version = int(bstr[idx:idx + 3], 2)
#             version_total += version
#             idx += 3
#             expect = 'typeID'
#         elif expect == 'typeID':
#             typeID = int(bstr[idx:idx + 3], 2)
#             print('type ID', typeID)
#             idx += 3
#             if typeID == 4:
#                 expect = 'literal'
#             else:
#                 expect = 'l_typeID'
#         elif expect == 'literal':
#             lflag = bstr[idx]
#             lpiece = bstr[idx + 1:idx + 5]
#             idx += 5
#             literal_str += lpiece
#             if lflag == '0':
#                 val = int(literal_str, 2)
#                 return val, idx
#         elif expect == 'l_typeID':
#             l_typeID = bstr[idx]
#             idx += 1
#             if l_typeID == '0':
#                 expect = 'nbits15'
#             elif l_typeID == '1':
#                 expect = 'npackets11'
#         elif expect == 'nbits15':
#             nbits = int(bstr[idx:idx + 15], 2)
#             idx += 15
#             old_idx = idx
#             vals, idx = get_packet_values(bstr, idx, nbits=nbits)
#             assert (idx == old_idx + nbits)
#             return operators[typeID](vals), idx
#         elif expect == 'npackets11':
#             npackets = int(bstr[idx:idx + 11], 2)
#             idx += 11
#             vals, idx = get_packet_values(bstr, idx, npackets=npackets)
#             assert (len(vals) == npackets)
#             return operators[typeID](vals), idx
#
#
# def get_packet_values(bstr, idx, nbits=None, npackets=None):
#     print('nbits/packets', nbits, npackets)
#     start_idx = idx
#     expect = 'version'
#     literal_str = ''
#     version_total = 0
#     operators = [sum, prod, min, max, None, gt, lt, eq]
#     e_len = {'version': 3, 'typeID': 3, 'literal': 5, 'l_typeID': 1, 'nbits15': 15, 'npackets11': 11}
#     packet_values = []
#     while (idx <= len(bstr) - e_len[expect]) and (nbits is None or idx < start_idx + nbits) \
#             and (npackets is None or len(packet_values) < npackets):
#         print('expect', expect)
#         if expect == 'version':
#             version = int(bstr[idx:idx + 3], 2)
#             version_total += version
#             idx += 3
#             expect = 'typeID'
#         elif expect == 'typeID':
#             typeID = int(bstr[idx:idx + 3], 2)
#             print('type ID', typeID)
#             idx += 3
#             if typeID == 4:
#                 expect = 'literal'
#             else:
#                 expect = 'l_typeID'
#             # print('idx ..', idx, len(bstr), e_len[expect])
#         elif expect == 'literal':
#             # print('literal piece', bstr[idx:idx+5])
#             lflag = bstr[idx]
#             lpiece = bstr[idx + 1:idx + 5]
#             idx += 5
#             literal_str += lpiece
#             if lflag == '0':
#                 val = int(literal_str, 2)
#                 # print('literal val', val)
#                 literal_str = ''
#                 packet_values.append(val)
#                 expect = 'version'
#         elif expect == 'l_typeID':
#             l_typeID = bstr[idx]
#             idx += 1
#             if l_typeID == '0':
#                 expect = 'nbits15'
#             elif l_typeID == '1':
#                 expect = 'npackets11'
#         elif expect == 'nbits15':
#             nbits = int(bstr[idx:idx + 15], 2)
#             idx += 15
#             old_idx = idx
#             vals, idx = get_packet_values(bstr, idx, nbits=nbits)
#             assert(idx == old_idx + nbits)
#             print('op', typeID, 'values', vals)
#             packet_values.append(operators[typeID](vals))
#             expect = 'version'
#         elif expect == 'npackets11':
#             npackets = int(bstr[idx:idx + 11], 2)
#             idx += 11
#             vals, idx = get_packet_values(bstr, idx, npackets=npackets)
#             print('there should be' , len(vals), 'values', vals)
#             assert (len(vals) == npackets)
#             print('op', typeID, 'values', vals)
#             packet_values.append(operators[typeID](vals))
#             expect = 'version'
#     return packet_values, idx
#
#
# print(get_packet_value(b_str))