from card import Card
from random import shuffle

class CardDeck:
    def __init__(self):
        self.__deck = self.generate_deck()
    
    def generate_deck(self):
        '''Gera um baralho embaralhado de cartas com base na quantidade de cartas de cada valor.'''
        
        number_of_cards = {1: 18, 2: 18, 3: 14, 4: 8, 5: 4, 6: 2, 7: 2}
        deck = []
        
        for card in number_of_cards.keys():
            for _ in range(number_of_cards[card]):
                deck.append(Card(card))
        
        shuffle(deck) # Embaralha o baralho
        
        return deck

    @property
    def deck(self):
        return self.__deck