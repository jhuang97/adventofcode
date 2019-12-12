class Moon:
	def __init__(self, pos):
		self.pos = pos
		self.vel = [0, 0, 0]

	def update_pos(self):
		self.pos = [self.pos[i] + self.vel[i] for i in range(3)]

	def disp(self):
		print(str(self.pos) + ' ' + str(self.vel))

	def pot_energy(self):
		return sum([abs(self.pos[i]) for i in range(3)])

	def kin_energy(self):
		return sum([abs(self.vel[i]) for i in range(3)])

	def energy(self):
		return self.pot_energy() * self.kin_energy()

def gravity_change(pos1, pos2): # change to be applied to planet 1 due to planet 2
	update = [None, None, None]
	for i in range(3):
		if pos1[i] == pos2[i]:
			update[i] = 0
		elif pos1[i] > pos2[i]:
			update[i] = -1
		elif pos1[i] < pos2[i]:
			update[i] = +1
	return update

def g_change_1d(pos1, pos2):
	if pos1 == pos2:
		return 0
	if pos1 > pos2:
		return -1
	if pos1 < pos2:
		return 1

class MoonSystem:
	def __init__(self, moonlist):
		self.moonlist = moonlist

	def update(self):
		gravity_list = [[0, 0, 0] for i in range(len(self.moonlist))]
		for i in range(len(self.moonlist)):
			for j in range(i+1, len(self.moonlist)):
				gchange = gravity_change(self.moonlist[i].pos, self.moonlist[j].pos)
				gravity_list[i] = [gravity_list[i][k] + gchange[k] for k in range(3)]
				gravity_list[j] = [gravity_list[j][k] - gchange[k] for k in range(3)]
		for i in range(len(self.moonlist)):
			self.moonlist[i].vel = [self.moonlist[i].vel[k] + gravity_list[i][k] for k in range(3)]
			self.moonlist[i].update_pos()

	def disp(self):
		for m in self.moonlist:
			m.disp()

	def total_energy(self):
		return sum([self.moonlist[i].energy() for i in range(len(self.moonlist))])

class OneDSys:
	def __init__(self, pos):
		self.pos = pos
		self.vel = [0 for i in range(len(pos))]

	def update(self):
		deltav = [0 for i in range(len(self.pos))]
		for i in range(len(self.pos)):
			for j in range(i+1, len(self.pos)):
				gchange = g_change_1d(self.pos[i], self.pos[j])
				deltav[i] += gchange
				deltav[j] -= gchange
		self.vel = [self.vel[i] + deltav[i] for i in range(len(self.pos))]
		self.pos = [self.pos[i] + self.vel[i] for i in range(len(self.pos))]

	def equals(self, other):
		return self.pos == other.pos and self.vel == other.vel

	def to_tuple(self):
		return tuple(self.pos + self.vel)

if __name__ == '__main__':
	# init_pos = [[-1, 0, 2],[2, -10, -7],[4, -8, 8],[3, 5, -1]]
	init_pos = [[0, 4, 0],[-10, -6, -14],[9, -16, -3],[6, -1, 2]]
	ml = MoonSystem([Moon(init_pos[i]) for i in range(len(init_pos))])

	ml.disp()

	for i in range(1000):
		ml.update()
		# ml.disp()

	print(ml.total_energy())

	# lol i wrote all that object-oriented stuff for nothing

	# part 2
	import copy
	for sub in range(3):
		print('component %d' % sub)
		spos = [moon[sub] for moon in init_pos]
		osys = OneDSys(spos)

		hist = {}
		hist[osys.to_tuple()] = 0
		repeat = False

		count = 0
		while not repeat:
			osys.update()
			# print(str(osys.pos) + ', ' + str(osys.vel))
			count += 1
			if osys.to_tuple() in hist:
				print('repeat %d %d' % (hist[osys.to_tuple()], count))
				repeat = True
			hist[osys.to_tuple()] = i