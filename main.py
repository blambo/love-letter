import random
from game import *
from dumb import Dumb
from blambo import Blambo
from reasonable import Reasonable

players = [Reasonable(), Reasonable(), Reasonable(), Blambo()]
wins = {}
for p in players:
  wins[p] = 0

try:

  num = 1
  while True:
    print '---------- GAME %d -----------' % num

    shuffled = list(players)
    random.shuffle(shuffled)
    winner = play_game(shuffled)

    print 'WINNER: ', winner
    wins[winner] += 1

    print
    num += 1

except KeyboardInterrupt:
  print
  print '========== WINS ==========='
  for p in players:
    print p.get_brain_name(), '-', wins[p], 'wins'
