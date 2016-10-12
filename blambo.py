from game import Player, Move, targetting_cards

class Blambo(Player):
  """
  Minimally viable player
  """
  def get_brain_name(self):
    return 'blambo'

  def new_game(self, initial_card, other_players):
    self.current_card = initial_card
    self.others = other_players
    self.count = self.generateCount()
    self.count[initial_card] = self.count[initial_card] - 1

  def decide_turn(self, card, **info):
    player = None

    # Update card counting
    self.count[card] = self.count[card] - 1

    #
    # Choose card
    #
    # Don't break the rulezz
    if self.current_card == 7 and card in [5,6]:
      self.current_card, card = card, 7
    elif self.current_card in [5,6] and card == 7:
      card = card # noop

    # Avoid committing suicide
    elif card == 8:
      card = self.swapWithCurrentCard(card)

    # Play the handmaiden
    elif card == 4:
      card = card # noop

    # Lower risk of suicide
    elif card == 3 and self.current_card < 4:
      card = self.swapWithCurrentCard(card)
    elif self.current_card == 3 and card > 4:
      card = self.swapWithCurrentCard(card)

    # Try to keep higher valued cards
    elif card > self.current_card:
      card = self.swapWithCurrentCard(card)


    #
    # Extras depending on chosen card
    #
    # Guess a card if we're playing the guard
    guess = None
    if card == 1:
      if self.count[3] > 0:
        guess = 3 # It is always the baron
      else:
        keys = self.count.keys()
        for key in keys:
          if key > 1 and self.count[key] > 0:
            guess = key
        if guess == None:
          guess = 2 # Except when it isn't

    # Choose player to target
    if card in targetting_cards:
      player = self.chooseTarget(info['immune'], card)

    return Move("im a little smarter!", card, player, guess)

  def player_discarded(self, player, card):
    self.count[card] = self.count[card] - 1

#  def player_moved(self, player, move):
#    pass
#
  def player_revealed(self, player, card):
    pass

  def replace_card(self, card):
    self.current_card = card

  def player_dead(self, player, last_card):
    self.others.remove(player)

  # Helper methods
  def generateCount(self):
    return {
      1: 5,
      2: 2,
      3: 2,
      4: 2,
      5: 2,
      6: 1,
      7: 1,
      8: 1
    }

  def chooseTarget(self, immune, card):
    available = [p for p in self.others if p not in immune]
    player = None
    if available:
      player = available[0]
    elif not available and card == 5:
      player = self
    return player

  def swapWithCurrentCard(self, card):
    temp = self.current_card
    self.current_card = card
    return temp

