from card import Card

class Player:
    def __init__(self, identifier: str):
        self.__cards = []
        self.__score = 0
        self.__identifier = identifier
        self.__turn = False
        self.__selected_card = None
    
    def select_card(self, card):
        if card in self.__cards:
            self.__selected_card = card
            return True
        else:
            return False

    def play_card(self, card):
        if card in self.__cards:
            self.__cards.remove(card)
            self.__selected_card = None
            return card
        else:
            return None

    def add_card(self, card):
        self.__cards.append(card)

    def update_score(self, points):
        self.__score += points
        
    @property
    def cards(self):
        return self.__cards
    
    @property
    def score(self):
        return self.__score
    
    @property
    def identifier(self):
        return self.__identifier
    
    @property
    def selected_card(self):
        return self.__selected_card