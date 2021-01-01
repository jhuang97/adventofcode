pub1 = 5764801
pub2 = 17807724
pub1 = 13233401
pub2 = 6552760


base = 20201227

def find_loop_size(num, base):
	test = 1
	power = 0
	while True:
		if test == num:
			return power
		test *= 7
		test %= base
		power += 1


l1 = find_loop_size(pub1, base)
l2 = find_loop_size(pub2, base)

print(l1)
print(l2)

enc = 1
for _ in range(l2):
	enc *= pub1
	enc %= base
print(enc)