import os
import random
from game import node, info
from cfr import cfr_player 
from human import human_player
cfr = cfr_player()
human = human_player()
cfr.load("M41.in")
cfr.normalize()
cfr.epsilon_adjust()
C0 = 2

def fight(players, node, dice, p):
	while not node.end():
		os.system('clear')
		print("Dice you have : " + str(node.count[p]) + "  Dice rival have : " + str(node.count[1 - p]))
		print("Your dice : " + ( str(node.state[0:node.count[0]]) if p == 0 else str(node.state[node.count[0]: node.count[0] + node.count[1]]) ))
		inf = node.to_info()
		act = players[1 - node.player].action(inf)
		if (1 - node.player != p):
			print("Opponent move : " + str(act))
		while not (act in node.getAllaction()):
			act = players[1 - node.player].action(inf)
		if (act == (-1, -1)):
			print(node.state)
		try:
			input("Press Enter to continue...")
		except:
			pass
		node.act(act, dice)
	return node.count[0] > 0


win = 0
for i in range(100):
	dice = [random.randint(1, 6) for x in range(100)]
	InitialState = node(
		[], [C0,C0], 
		node.draw([C0,C0], dice)
	)
	if random.randint(1,2) == 1:
		result = fight([human, cfr], InitialState, dice, 0)
	else:
		result = 1 - fight([cfr, human], InitialState, dice, 1)
	win = win + result
	if result == 1:
		print("You win " + str(win) + ":" + str(i + 1 - win))
	else:
		print("CFR win " + str(win) + ":" + str(i + 1 - win))
	try:
		input("Press Enter to continue...")
	except:
		pass
print("You win " + str(win) + " matches of all 100 matches")
