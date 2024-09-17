from board import Board
from card_deck import CardDeck
from player import Player
from game_interface import GameInterface

class GameController:
    def __init__(self):
        self.__board = Board()
        self.__local_player = Player("local")
        self.__remote_player = Player("remote")
        self.__deck = CardDeck()
        self.__interface = GameInterface(self)
    
    @property
    def board(self):
        return self.__board