class Board:
    def __init__(self):
        self.board = [[0 for _ in range(4)] for _ in range(4)]
        
    def update_board(self, board: list[int]):
        """Atualiza o tabuleiro."""
        
        self.board = board
        
    def get_line(self, i: int):
        """ Retorna a reta i do tabuleiro.
            0 <= i <= 3 : Retorna a linha i.
            4 <= i <= 7 : Retorna a coluna i-4.
            8 : Retorna a diagonal principal.
            9 : Retorna a diagonal secundária. 
        """
        
        # Retorna a linha i
        if i < 4:
            return self.board[i]
        
        # Retorna a coluna i-4
        elif i < 8:
            line = []
            for j in range(4):
                line.append(self.board[j][i-4])
            return line
        
        # Retorna a diagonal principal
        elif i == 8:
            line = []
            for j in range(4):
                line.append(self.board[j][j])
            return line
        
        # Retorna a diagonal secundária
        else:
            line = []
            for j in range(4):
                line.append(self.board[j][3-j])
            return line
    
    def put_card(self, card_number: int, i: int, j: int):
        """Coloca uma carta no tabuleiro."""
        
        self.board[i][j] = card_number
        
    def clear_line(self, i: int):
        """Remove uma linha, coluna ou diagonal do tabuleiro.
            0 <= i <= 3 : Remove a linha i.
            4 <= i <= 7 : Remove a coluna i-4.
            8 : Remove a diagonal principal.
            9 : Remove a diagonal secundária. 
        """
        
        if i < 4: # linhas
            self.board[i] = [0, 0, 0, 0]
        elif i < 8: # colunas
            for row in range(4):
                self.board[row][i - 4] = 0
        elif i == 8: # diagonal principal
            for x in range(4):
                self.board[x][x] = 0
        else: # diagonal secundaria
            for x in range(4):
                self.board[x][3 - x] = 0