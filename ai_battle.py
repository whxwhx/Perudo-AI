import os
import random
from game import node, info
from cfr import cfr_player
from human import human_player
C0 = 2
def fight(players, node, dice):
	while not node.end():
		inf = node.to_info()
		act = players[1 - node.player].action(inf)
		node.act(act, dice)
	return node.count[0] > 0

win = 0
player1 = cfr_player()
player1.load("M45.in")
player1.normalize()
player1.epsilon_adjust()
player2 = cfr_player()
player2.load("model.in")
player2.normalize()
turns = 10000
for i in range(turns):
	dice = [random.randint(1, 6) for x in range(100)]
	InitialState = node(
		[], [C0,C0], 
		node.draw([C0,C0], dice)
	)
	if random.randint(1,2) == 1:
		result = fight([player1, player2], InitialState, dice)
	else:
		result = 1 - fight([player2, player1], InitialState, dice)
	win = win + result
print("Player1 win " + str(win / turns))
try:
	input("Press Enter to continue...")
except:
	pass