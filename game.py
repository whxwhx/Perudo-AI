import random
import os
import copy
dice = []
history_len = 3
C0 = 2

class info:
	def __init__(self, h, c, s, l, p):
		self.history = copy.deepcopy(h) #to do
		self.count = copy.deepcopy(c)
		if p == 0: # if current player is player 1
			self.count[0], self.count[1] = self.count[1], self.count[0]
		self.state = s[0:c[0]] if p == 1 else s[c[0] : c[0] + c[1]]
		self.last = l

	def __eq__(self, another):
		return self.history == another.history and self.count == another.count and self.state == another.state and self.last == another.last

	def tostring(self):
		s = str(self.history) + '|' + str(self.count) + '|' + str(self.state) + '|' + str(self.last)
		return s

	def __hash__(self):
		return self.tostring().__hash__()

	def getAllaction(self):
		act = []
		tot = self.count[0] + self.count[1]
		l = len(self.history)
		if l: # if it's not the very first move
			last_bid = self.history[l - 1]
			act = [(-1, -1)] #call

			if last_bid[0] == 1:
				#increment 1
				for y in xrange(last_bid[1] + 1, tot + 1):
					act.append((1, y))
				#断言 another x
				if not self.last:  
					for x in xrange(2,7):
						for y in xrange(last_bid[1] * 2 + 1, tot + 1):
							act.append((x, y))
			else:
				if not self.last:
					#increment x
					for x in xrange(last_bid[0] + 1, 7):
						act.append((x, last_bid[1]))
					#attach 1
					for y in xrange((last_bid[1] + 1) / 2, tot + 1):
						act.append((1, y))
				#increment y
				for y in xrange(last_bid[1] + 1, tot + 1):
					act.append((last_bid[0], y))
		else:
			for x in xrange(1,7):
				for y in xrange(1,tot + 1):
					act.append((x, y))
		return act

def newinfo(h, c, s, l):
	InitialState = node(
		[], [C0,C0], 
		node.draw([C0,C0])
	)
	ans = InitialState.to_info()
	ans.history = h
	ans.count = c
	ans.state = s
	ans.last = l
	return ans

def compare(a, b):
	y1 = 2 * a[1] if a[0] != 1 else 4 * a[1] + 1
	y2 = 2 * b[1] if b[0] != 1 else 4 * b[1] + 1
	return y1 < y2 or (y1 == y2 and a[0] < b[0])
class node:
	def __init__(self, h, c, s):
		#[(a,b), (a,b), (a,b)]
		self.history = h
		#[a,b]
		self.count = c
		#[a,b,c,d,e,f,g,h,i,j]
		self.state = s
		self.last = 0
		self.player = 1 #who is the player that has just finished an operation

	def to_info(self):
		a = info(self.history, self.count, self.state, self.last, self.player)
		return a

	def __lt__(self, another):
		tot = self.count[0] + self.count[1]
		tot2 = another.count[0] + another.count[1]
		if tot > tot2:
			return 1
		elif tot == tot2:
			if len(self.history) < len(another.history):
				return 1
			elif len(self.history) > len(another.history):
				return 0
			else:
				if self.history == another.history:
					return 0
				else:
					return compare(self.history[0], another.history[0])
		else:
			return 0

	def __eq__(self, another):
		return self.history == another.history and self.count == another.count and self.state == another.state and self.last == another.last and self.player == another.player

	def tostring(self):
		s = str(self.history) + "|" + str(self.count) + "|" + str(self.state) + "|" + str(self.last) + "|" + str(self.player)
		return s

	def __hash__(self):
		return self.tostring().__hash__()

	def getAllaction(self):
		act = []
		tot = self.count[0] + self.count[1]
		l = len(self.history)
		if l:
			last_bid = self.history[l - 1]
			act = [(-1, -1)]

			if last_bid[0] == 1:
				#increment 1
				for y in xrange(last_bid[1] + 1, tot + 1):
					act.append((1, y))
				#断言 another x
				if not self.last:
					for x in xrange(2,7):
						for y in xrange(last_bid[1] * 2 + 1, tot + 1):
							act.append((x, y))
			else:
				if not self.last:
					#increment x
					for x in xrange(last_bid[0] + 1, 7):
						act.append((x, last_bid[1]))
					#attach 1
					for y in xrange((last_bid[1] + 1) / 2, tot + 1):
						act.append((1, y))
				#increment y
				for y in xrange(last_bid[1] + 1, tot + 1):
					act.append((last_bid[0], y))
		else:
			for x in xrange(1,7):
				for y in xrange(1,tot + 1):
					act.append((x, y))
		return act

	def act(self, action):
		l = len(self.history)
		if action == (-1, -1):
			last_bid = self.history[l - 1]
			tot = self.state.count(last_bid[0])
			if self.last == 0 and last_bid[0] != 1:
				tot = tot + self.state.count(1)

			win = self.player if tot >= last_bid[1] else 1 - self.player
			self.count[1 - win] = self.count[1 - win] - 1;
#			self.last = 1 if self.count[1 - win] == 1 else 0

			self.history = []
			if self.end():
				self.state = []
			else:
				self.state = self.draw(self.count)
		else:
			if l == history_len:
				self.history = self.history[1:]
			self.history.append(action)
		self.player = 1 - self.player

	def end(self):
		return self.count[0] == 0 or self.count[1] == 0;

	@staticmethod
	def draw(x):
		a = x[0]
		b = x[1]
		tot = a + b
		pre = (C0 * 2 + (tot + 1)) * (C0 * 2 - tot) / 2
		t1 = dice[pre: pre + a]
		t2 = dice[pre + a: pre + a + b]
		t1.sort()
		t2.sort()
		return t1 + t2

def search():
	InitialState = node(
		[], [5,5], 
		node.draw([5,5])
	)

	stack = [InitialState]
	searched_state = set()
	searched_state.add(InitialState)
	while len(stack):
		state = stack.pop()
		if state.end():
			continue
		for a in state.getAllaction():
			NewState = copy.deepcopy(state)
			NewState.act(a)
			if not (NewState in searched_state):
				stack.append(NewState)
				searched_state.add(NewState)
	
	print len(searched_state) + "states"

# bfs first to calculate the probability for two players to get to a node
# then calculate the utility and the regret value

strategy = dict() #info -> [[probility, regret, sumprobability]]
def bfs(S, T):
	q = [S]
	l = 0
	r = 1
	searched_state = set()
	searched_state.add(S)
	while l < r:
		state = q[l]
		if not state.end():
			for a in state.getAllaction():
				NewState = copy.deepcopy(state)
				NewState.act(a)
				if not (NewState in searched_state):
					q.append(NewState)
					searched_state.add(NewState)
					r = r + 1
		l = l + 1
	q.sort() 

	pos = dict() #node -> position
	for i in xrange(r):
		pos[q[i]] = i
	prob = [[0.0, 0.0] for x in xrange(r)]
	prob[0] = [1.0, 1.0]

#	try:
#		assert q[0] == S
#	except:
#		print q[0].tostring(), S.tostring(), q[0] <= S
#		raise ValueError
	for i in xrange(r):
		state = q[i]
		if state.end():
			continue
		L = state.getAllaction()
		length = len(L)
		inf = state.to_info()
		if strategy.get(inf) == None:
			strategy[inf] = [[1.0 / length, .0, .0] for x in xrange(length)]

		S = strategy[inf]
		cnt = 0
		for a in L:
			NewState = copy.deepcopy(state)
			NewState.act(a)
			t = pos[NewState]
#			try:
#				assert t > i
#			except:
#				print i, t
#				print q[i].tostring()
#				print q[t].tostring()
#				raise ValueError
			#probability for player 0 / 1 to reach some node
			prob[t][0] = prob[t][0] + prob[i][0] * (S[cnt][0] if NewState.player == 0 else 1)
			prob[t][1] = prob[t][1] + prob[i][1] * (S[cnt][0] if NewState.player == 1 else 1)
			cnt = cnt + 1
		

	prob.append([1.0, 1.0])

	utility = [0 for i in xrange(r)]
	L = range(r)
	L.reverse()
	for i in L:
#		print state.tostring()
		state = q[i]

		if state.end():
			#if current player wins, utility = 1.0 else -1.0
			utility[i] = 1.0 if state.count[state.player] == 0 else -1.0
		else:
			L = state.getAllaction()
			length = len(L)

			inf = state.to_info()
			S = strategy[inf]

			cnt = 0
			tmp = []
			for a in L:
				NewState = copy.deepcopy(state)
				NewState.act(a)
				t = pos[NewState]
				tmp.append(t)
				utility[i] = utility[i] - utility[t] * S[cnt][0] #utility[t] and i have different player
				cnt = cnt + 1

			#update regret
			tot = 0.0
			for j in xrange(length):
				t = tmp[j]
				S[j][1] = S[j][1] + (-utility[t] - utility[i]) * prob[i][state.player] #rival
				tot = tot + (S[j][1] if S[j][1] > 0 else 0)

			#get new strategy
			for j in xrange(length):
				S[j][0] = (1.0 / length) if tot == 0 else (S[j][1] / tot if S[j][1] > 0 else 0)
				if T > 20:
					S[j][2] = S[j][2] + S[j][0] * prob[i][1 - state.player] #self
	return utility[0]

def train(iteration):
	for t in xrange(iteration):
		global dice
		dice = [random.randint(1, 6) for x in xrange(100)]
		InitialState = node(
			[], [C0,C0], 
			node.draw([C0,C0])
		)
		if t % 200000 == 0:
			print "iteration", t, "utility", bfs(InitialState, iteration)

class player:
	def action(Info):
		raise NotImplemented

class random_player(player):
	def action(self, Info):
#		print "All feasiable action : " + str(Info.getAllaction())
		print "Your turn : ",
		try:
			a = input()
		except:
			a = (-2, -2)
		return a

class cfg_player(player):
	def action(self, Info):
		A = Info.getAllaction()
		if strategy.get(Info) == None:
			S = [1.0 / len(A) for x in xrange(len(A))]
		else:
			S = [x[2] for x in strategy[Info]]
		p = random.random()
		for i in xrange(len(A)):
			p = p - S[i]
			if p <= 0:
				print "Opponent move : " + str(A[i])
				return A[i]
		print "Opponent move : " + str(A[len(A) - 1])
		return A[len(A) - 1]

def fight(players, node, p):
	while not node.end():
		os.system('clear')
		print "Dice you have : " + str(node.count[p]) + "  Dice rival have : " + str(node.count[1 - p])
		print "Your dice : " + ( str(node.state[0:node.count[0]]) if p == 0 else str(node.state[node.count[0]: node.count[0] + node.count[1]]) )
		inf = node.to_info()
		act = players[1 - node.player].action(inf)
		while not (act in node.getAllaction()):
			act = players[1 - node.player].action(inf)
#		print act
		if (act == (-1, -1)):
			print node.state
		try:
			input("Press Enter to continue...")
		except:
			pass
		node.act(act)
	return node.count[0] > 0



def trans(s):
	s = s.strip(' ')
	s = s.strip('(')
	s = s.strip(')')
	if len(s) == 0:
		return tuple()
	else:
		return tuple([int(x) for x in s.split(',')])
def trans_tuple(s):
	s = s.strip('[')
	s = s.strip(']')
	if len(s) == 0:
		return []
	else:
		return [trans(x) for x in s.split('),')]

def trans_list(s):
	s = s.strip('[')
	s = s.strip(']')
	if len(s) == 0:
		return []
	else:
		return [int(x) for x in s.split(',')]

def read_model():
	f = open("model.in","r")
	l = int(f.readline())
	for i in xrange(l):
		if i % 100 == 0:
			print str(i) + " of " + str(l)
		s = f.readline()
		t = s.split('|')
		tmp = newinfo(trans_tuple(t[0]), trans_list(t[1]), trans_list(t[2]), int(t[3]))

		L = []
		length = int(f.readline())
		for j in xrange(length):
			L.append([0, 0, float(f.readline())])
		strategy[tmp] = L
	print "Reading finished"

read_model()


eps = 0.01
#train(200000 * 60 * 60)
#for key in strategy:
#	value = strategy[key]
#	norm = 0
#	L = len(value)
#	for p, r1, s in value:
#		norm = norm + s
#	cnt = 0
#	for p, r1, s in value:
#		value[cnt][2] = (1.0 / L) if norm == 0 else s / norm
#		cnt = cnt + 1

for key in strategy:
	value = strategy[key]
	norm = 0
	for p, r1, s in value:
		if s > eps:
			norm = norm + s
	cnt = 0
	for p, r1, s in value:
		value[cnt][2] = s / norm if s > eps else 0
		cnt = cnt + 1

#output strategy
#f = open("model_2.in", "w")
#f.write(str(len(strategy)) + '\n')
#for key in strategy:
#	value = strategy[key]
#	f.write(key.tostring() + '\n')
#	f.write(str(len(value)) + '\n')
#	for p, r1, s in value:
#		f.write(str(s) + '\n')
#		assert s <= 1

win = 0
for i in xrange(100):
	global dice
	player1 = cfg_player()
	player2 = random_player()
	dice = [random.randint(1, 6) for x in xrange(100)]
	InitialState = node(
		[], [C0,C0], 
		node.draw([C0,C0])
	)
	if random.randint(1,2) == 1:
		result = fight([player2, player1], InitialState, 0)
	else:
		result = 1 - fight([player1, player2], InitialState, 1)
	win = win + result
	if result == 1:
		print "You win " + str(win) + ":" + str(i + 1 - win)
	else:
		print "CFR win " + str(win) + ":" + str(i + 1 - win)
	try:
		input("Press Enter to continue...")
	except:
		pass
print "CFG win " + str(win) + " matches of all 100 matches"
