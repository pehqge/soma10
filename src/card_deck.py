from random import shuffle, choice

class CardDeck:
    def __init__(self):
        # Inicializa o deck
        self.deck = []
        
    def initialize_deck(self):
        """ Inicializa o deck."""
        # self.deck = [1] * 18 + [2] * 18 + [3] * 14 + [4] * 8 + [5] * 4 + [6] * 2 + [7] * 2
        for _ in range(18):
            self.deck.append(choice([1, 2, 3, 4, 5, 6, 7]))
        
        shuffle(self.deck)
        
    def update_deck(self, deck):
        """ Recebe um deck."""
        self.deck = deck
        
    def buy_card(self):
        """Retira uma carta do deck e a retorna."""
        
        if not self.deck: # Retorna None se o deck estiver vazio
            return None
        
        # Caso contrário, retira a carta do topo do deck
        card = self.deck.pop()
        return card
    
    def is_empty(self):
        """Retorna True se o deck estiver vazio, False caso contrário."""
        
        return not self.deck
        
    def reset(self):
        """ Reseta o deck."""
        self.deck = []