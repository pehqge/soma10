from random import shuffle

class CardDeck:
    def __init__(self):
        # Inicializa o deck
        self.deck = []
        self.size = 0
        
    def buy_card(self):
        """Retira uma carta do deck e a retorna."""
        
        if self.size == 0: # Retorna None se o deck estiver vazio
            return None
        
        # Caso contrário, retira a carta do topo do deck
        card = self.deck.pop()
        self.size -= 1
        return card
    
    def initialize_deck(self):
        """ Inicializa o deck."""
        self.deck = [1] * 18 + [2] * 18 + [3] * 14 + [4] * 8 + [5] * 4 + [6] * 2 + [7] * 2
        shuffle(self.deck)
        self.size = len(self.deck)
        
    def receive_deck(self, deck):
        """ Recebe um deck."""
        self.deck = deck
        self.size = len(deck)
        
    def reset(self):
        """ Reseta o deck."""
        self.deck = []
        self.size = 0