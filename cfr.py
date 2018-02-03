import random
import copy
from game import info, node
from player import  player
C0 = 2
eps_adj = 0.001

def newinfo(h, c, s, l):
	InitialState = node(
		[], [C0,C0], 
		node.draw([C0,C0], list(range(12)))
	)
	ans = InitialState.to_info()
	ans.history = h
	ans.count = c
	ans.state = s
	ans.last = l
	return ans

def trans_tuple(s):
	s = s.strip(' ')
	s = s.strip('(')
	s = s.strip(')')
	if len(s) == 0:
		return tuple()
	else:
		return tuple([int(x) for x in s.split(',')])

def trans_tuple_list(s):
	s = s.strip('[')
	s = s.strip(']')
	if len(s) == 0:
		return []
	else:
		return [trans_tuple(x) for x in s.split('),')]

def trans_number_list(s):
	s = s.strip('[')
	s = s.strip(']')
	if len(s) == 0:
		return []
	else:
		return [int(x) for x in s.split(',')]


class cfr_player():
	def __init__(self):
		self.strategy = dict()

	def action(self, Info):
		A = Info.getAllaction()
		if self.strategy.get(Info) == None:
			S = [1.0 / len(A) for x in range(len(A))]
		else:
			S = [x[2] for x in self.strategy[Info]]
		p = random.random()
		for i in range(len(A)):
			p = p - S[i]
			if p <= 0:
				return A[i]
		return A[len(A) - 1]

	def train(self, iteration):
		q = []
		prob = []
		pos = dict() #node -> position

		def bfs_all_states(S):
			nonlocal q
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
						NewState.act(a, dice)
						if not (NewState in searched_state):
							q.append(NewState)
							searched_state.add(NewState)
							r = r + 1
				l = l + 1
			q.sort() 

		def calculate_probability():
			nonlocal q
			nonlocal pos
			nonlocal prob
			n = len(q)
			for i in range(n):
				pos[q[i]] = i
			prob = [[0.0, 0.0] for x in range(n)]
			prob[0] = [1.0, 1.0]
			for i in range(n):
				state = q[i]
				if state.end():
					continue

				L = state.getAllaction()
				length = len(L)
				inf = state.to_info()
				if self.strategy.get(inf) == None:
					self.strategy[inf] = [[1.0 / length, .0, .0] for x in range(length)]
				S = self.strategy[inf]

				cnt = 0
				for a in L:
					NewState = copy.deepcopy(state)
					NewState.act(a, dice)
					t = pos[NewState]
					prob[t][0] = prob[t][0] + prob[i][0] * (S[cnt][0] if NewState.player == 0 else 1)
					prob[t][1] = prob[t][1] + prob[i][1] * (S[cnt][0] if NewState.player == 1 else 1)
					cnt = cnt + 1

		def update_regret():
			nonlocal q
			nonlocal pos
			nonlocal prob
			n = len(q)
			utility = [0 for i in range(n)]
			L = list(range(n))
			L.reverse()
			for i in L:
				state = q[i]
				if state.end():
					utility[i] = 1.0 if state.count[state.player] == 0 else -1.0
				else:
					L = state.getAllaction()
					length = len(L)

					inf = state.to_info()
					S = self.strategy[inf]

					cnt = 0
					tmp = []
					for a in L:
						NewState = copy.deepcopy(state)
						NewState.act(a, dice)
						t = pos[NewState]
						tmp.append(t)
						utility[i] = utility[i] - utility[t] * S[cnt][0] #utility[t] and i have different player
						cnt = cnt + 1

					#update regret
					tot = 0.0
					for j in range(length):
						t = tmp[j]
						S[j][1] = S[j][1] + (-utility[t] - utility[i]) * prob[i][state.player] #rival
						tot = tot + (S[j][1] if S[j][1] > 0 else 0)

					#get new strategy
					for j in range(length):
						S[j][0] = (1.0 / length) if tot == 0 else (S[j][1] / tot if S[j][1] > 0 else 0)
						if T > 100 * 200000:
							S[j][2] = S[j][2] + S[j][0] * prob[i][1 - state.player] #self
			return utility[0]

		tot = .0
		for T in range(iteration):
			dice = [random.randint(1, 6) for x in range(12)]
			InitialState = node(
				[], [C0,C0], 
				node.draw([C0,C0], dice)
			)
			bfs_all_states(InitialState)
			calculate_probability()
			tmp = update_regret()
			tot = tot + tmp
			if T % 10 == 0:
				print(str(T) + " iterations trained, utility : " + str(tot / 10.0))
			if T % (600) == 0:
				self.output("model_tmp" + str((T / (600 * 200000)) % 2) + ".in")
		self.normalize()

	def load(self, fn):
		f = open(fn,"r")
		l = int(f.readline())
		for i in range(l):
			if i % 100 == 0:
				print(str(i) + " of " + str(l) + " loaded")
			s = f.readline()
			t = s.split('|')
			tmp = newinfo(trans_tuple_list(t[0]), trans_number_list(t[1]), trans_number_list(t[2]), int(t[3]))

			L = []
			length = int(f.readline())
			for j in range(length):
				L.append([0, 0, float(f.readline())])
			self.strategy[tmp] = L
		print("load complete")

	def train_load(self, fn):
		f = open(fn,"r")
		l = int(f.readline())
		for i in range(l):
			if i % 100 == 0:
				print(str(i) + " of " + str(l) + " loaded")
			s = f.readline()
			t = s.split('|')
			tmp = newinfo(trans_tuple_list(t[0]), trans_number_list(t[1]), trans_number_list(t[2]), int(t[3]))

			L = []
			length = int(f.readline())
			for j in range(length):
				p = float(f.readline())
				L.append([p, p, p])
			self.strategy[tmp] = L
		print("load complete")

	def output(self, fn):
		f = open(fn, "w")
		f.write(str(len(self.strategy)) + '\n')
		for key in self.strategy:
			value = self.strategy[key]
			f.write(key.tostring() + '\n')
			f.write(str(len(value)) + '\n')
			for p, r1, s in value:
				f.write(str(s) + '\n')

	def normalize(self):
		for key in self.strategy:
			value = self.strategy[key]
			norm = 0
			L = len(value)
			for p, r1, s in value:
				norm = norm + s
			cnt = 0
			for p, r1, s in value:
				value[cnt][2] = (1.0 / L) if norm == 0 else s / norm
				cnt = cnt + 1

	def epsilon_adjust(self):
		for key in self.strategy:
			value = self.strategy[key]
			norm = 0
			for p, r1, s in value:
				if s > eps_adj:
					norm = norm + s
			cnt = 0
			for p, r1, s in value:
				value[cnt][2] = s / norm if s > eps_adj else 0
				cnt = cnt + 1