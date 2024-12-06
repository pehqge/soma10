from random import shuffle

class CardDeck:
    def __init__(self):
        self.deck = []
        
    def initialize_deck(self):
        """ Inicializa o deck."""
        
        # Deck original do jogo Soma10 (descrito nas regras do jogo)
        self.deck = [1] * 18 + [2] * 18 + [3] * 14 + [4] * 8 + [5] * 4 + [6] * 2 + [7] * 2
        
        # Embaralha o deck
        shuffle(self.deck) 
        
    def update_deck(self, deck):
        """ Recebe um deck."""
        
        self.deck = deck
        
    def buy_card(self):
        """Retira uma carta do deck e a retorna."""
        
        # Se o deck estiver vazio, retorna None
        if not self.deck:
            return None
        
        # Caso contrário, retira a carta do topo do deck
        card = self.deck.pop()
        return card
    
    def is_empty(self):
        """Retorna True se o deck estiver vazio, False caso contrário."""
        
        return not self.deck
