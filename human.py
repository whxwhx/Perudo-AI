import game
from player import player

def trans_tuple(s):
	s = s.strip(' ')
	s = s.strip('(')
	s = s.strip(')')
	if len(s) == 0:
		return tuple()
	else:
		return tuple([int(x) for x in s.split(',')])

class human_player():
	def action(self, Info):
		print("Your turn : ", end="")
		try:
			a = trans_tuple(input())
		except:
			a = (-2, -2)
		return a
