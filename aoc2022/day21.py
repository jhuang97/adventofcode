import numpy as np

file = open('day21_in.txt', 'r')
# file = open('day21_test.txt', 'r')
lines = file.read().strip().splitlines()

str_dict = {}
for l in lines:
	parts = l.split(': ')
	str_dict[parts[0]] = parts[1].split()

# print(str_dict)


val_dict = {}

def get_val(name):
	if name in val_dict:
		return val_dict[name]
	
	str_def = str_dict[name]
	if len(str_def) == 1:
		val = int(str_def[0])
	elif len(str_def) == 3:
		val1 = get_val(str_def[0])
		val2 = get_val(str_def[2])
		if str_def[1] == '+':
			val = val1 + val2
		elif str_def[1] == '-':
			val = val1 - val2
		elif str_def[1] == '*':
			val = val1 * val2
		elif str_def[1] == '/':
			val = val1 / val2
		else:
			print('oh no')
	else:
		print('oh no')
	val_dict[name] = val
	return val


print(get_val('root'))


val_dict2 = {}
def get_val2(name):
	if name in val_dict2:
		return val_dict2[name]

	if name == 'humn':
		val = ('humn',)
	else:
		str_def = str_dict[name]
		if len(str_def) == 1:
			val = int(str_def[0])
		elif len(str_def) == 3:
			val1 = get_val2(str_def[0])
			val2 = get_val2(str_def[2])
			if isinstance(val1, tuple) or isinstance(val2, tuple):
				val = (str_def[1], val1, val2)
			else:
				if str_def[1] == '+':
					val = val1 + val2
				elif str_def[1] == '-':
					val = val1 - val2
				elif str_def[1] == '*':
					val = val1 * val2
				elif str_def[1] == '/':
					val = val1 / val2
				else:
					print('oh no')
		else:
			print('oh no')

	val_dict2[name] = val
	return val


root_res = get_val2('root')
eqn = (root_res[1], root_res[2])


def try_simplify(eqn):
	changed = False
	if isinstance(eqn[0], tuple) and len(eqn[0]) == 3:
		op, oprd1, oprd2 = eqn[0]
		is_t1, is_t2 = isinstance(oprd1, tuple), isinstance(oprd2, tuple)
		if op == '/':
			if not is_t2:
				eqn = oprd1, oprd2 * eqn[1]
				changed = True
		elif op == '+':
			if is_t1 and not is_t2:
				eqn = oprd1, eqn[1] - oprd2
				changed = True
			elif is_t2 and not is_t1:
				eqn = oprd2, eqn[1] - oprd1
				changed = True
		elif op == '*':
			if is_t1 and not is_t2:
				eqn = oprd1, eqn[1] / oprd2
				changed = True
			elif is_t2 and not is_t1:
				eqn = oprd2, eqn[1] / oprd1
				changed = True
		elif op == '-':
			if is_t1 and not is_t2:
				eqn = oprd1, eqn[1] + oprd2
				changed = True
			elif is_t2 and not is_t1:
				eqn = oprd2, oprd1 - eqn[1]
				changed = True

	return eqn, changed


# print(eqn)
while True:
	eqn, changed = try_simplify(eqn)

	# print(eqn[0], '==', eqn[1])
	if not changed:
		break
# print(val_dict2)

print(eqn[1])