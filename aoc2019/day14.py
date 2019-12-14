import itertools
import math

def parse_quantity(instr):
	strs = instr.split(' ')
	return (int(strs[0]), strs[1])

def parse_reactions(instr):
	instrs = instr.split('\n')
	tokens = {'ORE':0, 'FUEL':1}
	rxns = [line.split(' => ') for line in instrs]

	# first, get names of all chemicals and store in tokens
	tidx = 2
	for line in rxns:
		for side in line:
			for qstr in side.split(', '):
				cname = parse_quantity(qstr)[1]
				if cname not in tokens:
					tokens[cname] = tidx
					tidx += 1

	rxn_matrix = [[0 for i in range(len(tokens))] for j in range(len(rxns))]
	for i in range(len(rxns)):
		line = rxns[i]
		for qstr in line[0].split(', '):
			qtuple = parse_quantity(qstr)
			rxn_matrix[i][tokens[qtuple[1]]] = -qtuple[0]

		qtuple = parse_quantity(line[1])
		rxn_matrix[i][tokens[qtuple[1]]] = qtuple[0]

	return (rxn_matrix, tokens)

def calc_ore(rxn_matrix, v_rxn):
	n_chem = len(rxn_matrix[0])

	# done = False
	while True:
		# identify who needs help
		need_help = []
		for i in range(1, n_chem):
			if v_rxn[i] < 0:
				need_help.append(i)
		if len(need_help) == 0:
			break
		i_make = need_help[0]
		for i in range(len(rxn_matrix)):
			if rxn_matrix[i][i_make] > 0:
				break
		num_make = math.ceil((-v_rxn[i_make])/rxn_matrix[i][i_make])
		v_rxn = [v_rxn[j] + num_make * rxn_matrix[i][j] for j in range(n_chem)]
		# print(str(v_rxn))

	return (-v_rxn[0], v_rxn)


def solve_ore(rxn_matrix):
	n_chem = len(rxn_matrix[0])
	v_rxn = [0 for i in range(n_chem)]
	v_rxn[1] = -1

	return calc_ore(rxn_matrix, v_rxn)

if __name__ == '__main__':
	instr = """10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL"""

	instr = """9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL"""

	instr13 = """157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""

	instrMain = """2 KBRD => 3 NSPQ
1 TMTNM, 5 WMZD => 4 JVBK
3 TMTNM => 8 JTPF
3 NDXL => 2 BDQP
2 VTGNT => 2 TNWR
1 ZQRBC => 2 WGDN
2 MJMC => 3 QZCZ
10 MDXVB, 3 DHTB => 1 SRLP
1 KBRD, 1 PNPW => 6 SQCB
1 KDTRS, 4 VTGNT => 7 NDXL
1 FZSJ => 1 CJPSR
6 TKMKD => 8 FTND
2 ZNBSN => 4 DNPT
16 SKWKQ, 2 FZSJ, 3 GSQL, 1 PNRC, 4 QNKZW, 4 RHZR, 10 MTJF, 1 XHPK => 3 RJQW
1 NHQW => 8 QNKZW
16 JZFCN, 9 KWQSC, 1 JGTR => 7 TMTNM
2 PNRC => 7 LCZD
1 NLSNC, 14 SXKC, 2 DHTB => 1 ZQRBC
1 MXGQ, 2 KWQPL => 3 FZSJ
6 DWKLT, 1 VHNXW, 3 NSPQ => 1 BQXNW
23 KDTRS => 1 XHPK
1 PFBF, 3 KBLHZ => 3 MBGWZ
5 NSPQ => 3 TPJP
27 SRLP, 12 KWQSC, 14 ZNBSN, 33 HQTPN, 3 HWFQ, 23 QZCZ, 6 ZPDN, 32 RJQW, 3 GDXG => 1 FUEL
2 NSPQ, 5 ZNBSN, 1 TPJP => 8 PFBF
1 MSCRZ => 3 ZNBSN
1 TNWR, 2 ZNBSN => 5 MDXVB
10 SQCB => 5 MXGQ
3 JVBK, 1 MTJF, 1 KBLHZ => 2 HQTPN
2 MJMC => 2 KMLKR
2 BQXNW, 1 CJPSR, 25 KWQPL => 4 PNRC
1 VHNXW, 3 KWZKV => 4 TKMKD
10 VTGNT, 4 JTPF => 9 KWZKV
168 ORE => 3 JZFCN
173 ORE => 5 KBRD
2 TNWR, 1 MBGWZ, 3 NSPQ => 8 SKWKQ
1 KWZKV, 2 MJMC, 14 SKWKQ => 9 NSTR
4 JZFCN, 13 PNPW => 2 WMZD
6 JQNGL => 6 MGFZ
1 SQCB, 4 NLSNC => 5 DHTB
5 MGFZ, 39 WGDN, 1 MBGWZ, 2 NSTR, 1 XKBND, 1 SXKC, 1 JVBK => 5 ZPDN
7 NSPQ, 6 PNPW => 7 NLSNC
3 TNWR => 9 KWQPL
9 NLSNC, 4 NDXL, 1 MDXVB => 4 MTJF
2 VTJC => 7 PNPW
2 JZFCN => 8 MSCRZ
134 ORE => 3 JGTR
3 HQTPN => 4 GSQL
154 ORE => 9 VTJC
1 KWQSC, 14 KBRD => 4 JQCZ
7 PNRC, 1 XKBND => 8 RHZR
1 JQCZ => 4 VTGNT
6 BDQP => 6 JQNGL
7 FTND => 3 XKBND
2 XHPK, 4 NHQW => 1 MJMC
1 JQCZ => 5 KDTRS
1 DNPT => 4 KBLHZ
1 KMLKR, 26 ZNBSN, 1 LCZD, 11 QNKZW, 2 SQCB, 3 FTND, 24 PNRC => 4 HWFQ
179 ORE => 6 KWQSC
2 TKMKD, 3 FZSJ => 2 SXKC
2 JTPF => 7 VHNXW
1 FTND => 7 DWKLT
13 TNWR, 2 QNKZW, 6 SQCB => 5 GDXG
5 JTPF, 4 ZNBSN, 8 WMZD => 8 NHQW"""
	
	# 143173 ore for 1 fuel

	rxn_matrix, tokens = parse_reactions(instrMain)
	for row in rxn_matrix:
		print(str(row))

	print(tokens)
	ore_per_fuel, ore_rxn = solve_ore(rxn_matrix)
	print('need %d ore' % ore_per_fuel)
	print(str(ore_rxn))

	trillion = 1000000000000

	ore_rxn = [0 for i in range(len(ore_rxn))]
	ore_rxn[0] = trillion

	import copy
	count = 0
	step_size = 100000
	while True:
		old_ore_rxn = copy.deepcopy(ore_rxn)
		ore_rxn[1] -= step_size
		neg_ore, ore_rxn = calc_ore(rxn_matrix, copy.deepcopy(ore_rxn))
		if neg_ore > 0 and step_size == 1:
			break
		if neg_ore > 0:
			ore_rxn = old_ore_rxn # restore from backup after failed run
			step_size //= 10 # adaptive step size reduction
			print('step %d' % step_size)
		else:
			count += step_size
		print(str(ore_rxn))

	print(count)