class Player:
    def __init__(self, identifier):
        self.identifier = identifier
        self.score = 0
        self.cards = []
        self.selected_card = None
        self.turn = False
        
    def add_card(self, card):
        self.cards.append(card)
        
    def remove_card(self, card):
        self.cards.remove(card)
        self.selected_card = None
        
    def select_card(self, card):
        self.selected_card = card
        
    def add_score(self, score):
        self.score += score
        
    def reset(self):
        self.score = 0
        self.cards = []
        self.selected_card = None
        self.turn = False