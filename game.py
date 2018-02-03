import random
import os
import copy
history_len = 3
C0 = 2

class situation:
	def __init__(self):
		self.history = [] #to do
		self.count = []
		self.state = []
		self.last = 0

	def getAllaction(self):
		act = []
		tot = self.count[0] + self.count[1]
		l = len(self.history)
		if l: # if it's not the very first move
			last_bid = self.history[l - 1]
			act = [(-1, -1)] #call

			if last_bid[0] == 1:
				#increment 1
				for y in range(last_bid[1] + 1, tot + 1):
					act.append((1, y))
				#断言 another x
				if not self.last:  
					for x in range(2,7):
						for y in range(last_bid[1] * 2 + 1, tot + 1):
							act.append((x, y))
			else:
				if not self.last:
					#increment x
					for x in range(last_bid[0] + 1, 7):
						act.append((x, last_bid[1]))
					#attach 1
					for y in range((last_bid[1] + 1) // 2, tot + 1):
						act.append((1, y))
				#increment y
				for y in range(last_bid[1] + 1, tot + 1):
					act.append((last_bid[0], y))
		else:
			for x in range(1,7):
				for y in range(1,tot + 1):
					act.append((x, y))
		return act

class info(situation):
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

def compare(a, b):
	y1 = 2 * a[1] if a[0] != 1 else 4 * a[1] + 1
	y2 = 2 * b[1] if b[0] != 1 else 4 * b[1] + 1
	return y1 < y2 or (y1 == y2 and a[0] < b[0])
	
class node(situation):
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

	def act(self, action, dice):
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
				self.state = self.draw(self.count, dice)
		else:
			if l == history_len:
				self.history = self.history[1:]
			self.history.append(action)
		self.player = 1 - self.player

	def end(self):
		return self.count[0] == 0 or self.count[1] == 0;

	@staticmethod
	def draw(x, dice):
		a = x[0]
		b = x[1]
		tot = a + b
		pre = (C0 * 2 + (tot + 1)) * (C0 * 2 - tot) // 2
		t1 = dice[pre: pre + a]
		t2 = dice[pre + a: pre + a + b]
		t1.sort()
		t2.sort()
		return t1 + t2