from random import shuffle

class CardDeck:
    def __init__(self):
        # Inicializa o deck de acordo com as regras oficiais do jogo
        self.deck = [1] * 18 + [2] * 18 + [3] * 14 + [4] * 8 + [5] * 4 + [6] * 2 + [7] * 2
        
        # Embaralha o deck
        shuffle(self.deck)
        
        # Inicializa o tamanho do deck
        self.size = len(self.deck)
        
    def buy_card(self):
        """Retira uma carta do deck e a retorna."""
        
        if self.size == 0: # Retorna None se o deck estiver vazio
            return None
        
        # Caso contrário, retira a carta do topo do deck
        card = self.deck.pop()
        self.size -= 1
        return card
    
    def reset_deck(self):
        """ Reinicia o deck."""
        
        self.deck = [1] * 18 + [2] * 18 + [3] * 14 + [4] * 8 + [5] * 4 + [6] * 2 + [7] * 2
        shuffle(self.deck)
        self.size = len(self.deck)

    def update_deck(self, cards):
        """ Atualiza deck"""
        self.deck = cards
        self.size = len(self.deck)

    def empty(self):
        """ Checa se o baralho está vazio """
        if len(self.deck) > 0:
            return False
        return True