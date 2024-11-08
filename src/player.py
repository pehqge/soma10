class Player:
    def __init__(self, identifier: str):
        self.cards = []
        self.score = 0
        self.identifier = identifier
        self.turn = False
        self.selected_card = None
        
    def add_card(self, card: int):
        """Adiciona uma carta à mão do jogador."""
        
        self.cards.append(card)
        
    def remove_card(self, card: int):
        """Remove uma carta da mão do jogador."""
        
        self.cards.remove(card)
        self.selected_card = None
        
    def select_card(self, card: int):
        """Indica uma carta como a seleção do jogador."""
        
        self.selected_card = card
        
    def add_score(self, score: int):
        """Atualiza o score do jogador."""
        
        self.score += score
        
    def reset(self):
        """Reseta o jogador."""
        
        self.score = 0
        self.cards = []
        self.selected_card = None
        self.turn = False