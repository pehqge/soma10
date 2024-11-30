class Player:
    def __init__(self, name: str, id: str):
        self.cards = []
        self.card_number = 0
        self.score = 0
        self.name = name
        self.id = id
        self.turn = False
        self.selected_card = None
        self.won = None
    
    def get_cards(self):
        return self.cards
    
    def update_score(self, score: int):
        self.score = score
    
    def update_hand(self, cards: list):
        self.cards = cards
    
    def update_info(self, info: list):
        self.name = info[0]
        self.id = info[1]
        
    def update_card_number(self, card_number: int):
        self.card_number = card_number
        
    def add_card(self, card: int):
        """Adiciona uma carta à mão do jogador."""
        
        self.cards.append(card)
        self.card_number += 1
        
    def remove_card(self, card: int):
        """Remove uma carta da mão do jogador."""
        
        self.cards.remove(card)
        self.card_number -= 1
        
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
        self.card_number = 0
        self.selected_card = None
        self.turn = False