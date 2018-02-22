import os
import random
from game import node, info
from cfr import cfr_player
from human import human_player
C0 = 2
player = cfr_player()
player.train(60 * 60 * 4 * 60)
player.output("test.QAQ")