class Player:
    def __init__(self, name: str, id: str):
        self.cards = []
        self.card_number = 0
        self.score = 0
        self.name = name
        self.id = id
        self.turn = False
        self.chosen_card = None
        self.won_game = False
    
    def get_cards(self):
        """Retorna as cartas do jogador."""
        
        return self.cards
    
    def update_score(self, score: int):
        """Atualiza o score do jogador."""
        
        self.score = score
    
    def update_hand(self, cards: list):
        """Atualiza as cartas do jogador."""
        
        self.cards = cards
    
    def update_info(self, info: list):
        """Atualiza as informações do jogador."""
        
        self.name = info[0]
        self.id = info[1]
        
    def update_card_number(self, card_number: int):
        """Atualiza o número de cartas do jogador."""
        
        self.card_number = card_number
        
    def add_card(self, card: int):
        """Adiciona uma carta à mão do jogador."""
        
        self.cards.append(card)
        self.card_number += 1
        
    def remove_card(self, card: int):
        """Remove uma carta da mão do jogador."""
        
        self.cards.remove(card)
        self.card_number -= 1
        
    def choose_card(self, card: int):
        """Indica uma carta como a seleção do jogador."""
        
        self.chosen_card = card
        
    def add_score(self, score: int):
        """Atualiza o score do jogador."""
        
        self.score += score
        
    def attribute_victory(self):
        """Atribui a vitória ao jogador."""
        
        self.won_game = True