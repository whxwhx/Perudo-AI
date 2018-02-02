import game
import player
class human_player(player):
	def action(self, Info):
		print "Your turn : ",
		try:
			a = input()
		except:
			a = (-2, -2)
		return a
