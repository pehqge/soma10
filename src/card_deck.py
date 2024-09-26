from random import shuffle

class CardDeck:
    def __init__(self):
        self.deck = [1] * 18 + [2] * 18 + [3] * 14 + [4] * 8 + [5] * 4 + [6] * 2 + [7] * 2
        self.shuffle()
        self.size = len(self.deck)
        
    def shuffle(self):
        shuffle(self.deck)  # Embaralha a lista in place
        
    def buy_card(self):
        if self.size == 0:
            return None
        
        card = self.deck.pop()
        self.size -= 1
        return card
    
    def reset_deck(self):
        self.deck = [1] * 18 + [2] * 18 + [3] * 14 + [4] * 8 + [5] * 4 + [6] * 2 + [7] * 2
        self.shuffle()
        self.size = len(self.deck)