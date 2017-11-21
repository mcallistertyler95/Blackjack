from random import shuffle
class Cards():
  def __init__(self, value, suit):
    self.value = value
    self.suit = suit
  
  def getCardValue(self):
    if(self.value == "Ace"):
      return 11
    elif(self.value == "Jack" or self.value == "Queen" or self.value == "King"):
      return 10
    else:
      return int(self.value)
  
  def printCard(self):
    print("Card:", self.value, "of", self.suit)
  
  def compareCardValue(self, other):
    return self.getCardValue() > other.getCardValue()
    
class Deck():
  def __init__(self):
    self.deck = []
    self.suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
    self.value = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10","Jack", "Queen", "King"]
    self.insertCards()
    
  def insertCards(self):
    for x in range(0, len(self.suits)):
      for y in range(0, len(self.value)):
        self.deck.append(Cards(str(self.value[y]),str(self.suits[x])))
  
  def releaseTopCard(self):
    return self.deck.pop()
        
  def showAllCards(self):
    noCards = 0
    for x in range(0, len(self.deck)):
      noCards = noCards + 1
      self.deck[x].printCard()
    print("Number of cards in deck:", noCards)
    
  def shuffleDeck(self):
    shuffle(self.deck)

class Hand():
  def __init__(self, name):
    self.held = []
    self.name = name
  
  def showHand(self):
    print("-----------")
    print("Current cards in",self.name,"hand:")
    for x in range(0, len(self.held)):
      self.held[x].printCard()
    print("Total:", self.handTotal())
    print("-----------")
  
  def handTotal(self):
    total = 0
    for x in range(0, len(self.held)):
      total = total + self.held[x].getCardValue()
    return total
    
  def draw(self, number, Deck):
    for _ in range(0, number):
      self.held.append(Deck.releaseTopCard())
    
  def gameState(self, other):
    if self.handTotal() > other.handTotal() and self.bustCheck() == False:
      print("Dealer wins!")
      return True
    elif self.handTotal() < other.handTotal() and other.bustCheck() == False:
      print("Game State - You win")
      return True
    elif self.handTotal() == other.handTotal() and self.bustCheck() == False:
      print("Draw")
      return True
    else:
      return self.bustCheck()

  def bustCheck(self):
    if self.handTotal() > 21:
      print("Bust, game over")
      return True
    elif self.handTotal() == 21:
      print("Blackjack!")
      return True
    elif self.handTotal() < 21:
      return False

def main():
  gameOver = False
  #Main game loop
  new_deck = Deck()
  new_deck.shuffleDeck()
  new_hand = Hand("Dealer")
  player_hand = Hand("Player")
  new_hand.draw(2, new_deck) ##draw 5 cards from the deck
  player_hand.draw(2, new_deck)
  player_hand.showHand()
  new_hand.showHand()
  while gameOver == False:
    action = input("Hit or stand?")
    if action == "hit":
      player_hand.draw(1, new_deck)
      player_hand.showHand()
      gameOver = player_hand.bustCheck()
      if gameOver == True:
        break
      if new_hand.handTotal() < 17:
        new_hand.draw(1, new_deck)
        gameOver = new_hand.bustCheck()
        new_hand.showHand()
        if gameOver == True:
          break
    elif action == "stand":
      if new_hand.handTotal() < 17:
        new_hand.draw(1, new_deck)
        gameOver = new_hand.bustCheck()
        new_hand.showHand()
        if gameOver == True:
          break
      if new_hand.handTotal() >= 17:
        gameOver = new_hand.gameState(player_hand)
        if gameOver == True:
          break
    
main()