import game
import player
import cfr
import human
cfr = cfr_player()
human = human_player()
cfr.load("model.in")
dice = []

def fight(players, node, p):
	while not node.end():
		os.system('clear')
		print "Dice you have : " + str(node.count[p]) + "  Dice rival have : " + str(node.count[1 - p])
		print "Your dice : " + ( str(node.state[0:node.count[0]]) if p == 0 else str(node.state[node.count[0]: node.count[0] + node.count[1]]) )
		inf = node.to_info()
		act = players[1 - node.player].action(inf)
		while not (act in node.getAllaction()):
			act = players[1 - node.player].action(inf)
		if (act == (-1, -1)):
			print node.state
		try:
			input("Press Enter to continue...")
		except:
			pass
		node.act(act, dice)
	return node.count[0] > 0


win = 0
for i in xrange(100):
	global dice
	dice = [random.randint(1, 6) for x in xrange(100)]
	InitialState = node(
		[], [C0,C0], 
		node.draw([C0,C0])
	)
	if random.randint(1,2) == 1:
		result = fight([human, cfr], InitialState, 0)
	else:
		result = 1 - fight([cfr, human], InitialState, 1)
	win = win + result
	if result == 1:
		print "You win " + str(win) + ":" + str(i + 1 - win)
	else:
		print "CFR win " + str(win) + ":" + str(i + 1 - win)
	try:
		input("Press Enter to continue...")
	except:
		pass
print "You win " + str(win) + " matches of all 100 matches"
