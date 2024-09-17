from card import Card

class Board:
    def __init__(self):
        self.__board = [[Card(0) for _ in range(4)] for _ in range(4)]
        
    def insert_card(self, row: int, col: int, card: Card):
        if not isinstance(card, Card):
            raise TypeError("O argumento 'card' deve ser uma instância da classe Card.")
        
        else:
            self.__board[row][col] = card
            
    def remove_row(self, row: int):
        self.__board[row] = [Card(0) for _ in range(4)]
        
    def remove_col(self, col: int):
        for row in range(4):
            self.__board[row][col] = Card(0)
            
    def remove_diagonal(self, type: str):
        if type == "primary":
            for i in range(4):
                self.__board[i][i] = Card(0)
                
        elif type == "secondary":
            for i in range(4):
                self.__board[i][3 - i] = Card(0)
                
        else:
            raise ValueError("O argumento 'type' deve ser 'primary' ou 'secundary'.")
            
    @property
    def board(self):
        return self.__board