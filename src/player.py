class Player:
    def __init__(self, name: str, id: str):
        self.cards = []
        self.score = 0
        self.name = name
        self.id = id
        self.turn = False
        self.selected_card = None
        self.won = None
        
    def update_info(self, name: str, id: str):
        self.name = name
        self.id = id
        
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
        
        self.id = None
        self.name = None
        self.score = 0
        self.cards = []
        self.selected_card = None
        self.turn = False