class Board:
    def __init__(self):
        # Inicializa o board 4x4 vazio
        self.board = [[0 for _ in range(4)] for _ in range(4)]
    
    def put_card(self, card_number: int, i: int, j: int):
        """Coloca uma carta no tabuleiro."""
        
        self.board[i][j] = card_number
        
    def remove(self, i: int):
        """Remove uma linha, coluna ou diagonal do tabuleiro."""
        
        if i < 4: # linhas
            self.board[i] = [0, 0, 0, 0]
        elif i < 8: # colunas
            for row in range(4):
                col = i - 4
                self.board[row][col] = 0
        else: # diagonais
            if i == 8: # diagonal principal
                for x in range(4):
                    self.board[x][x] = 0
            if i == 9: # diagonal secundaria
                for x in range(4):
                    self.board[x][3 - x] = 0

    def reset(self):
        """Reinicia o tabuleiro voltando tudo para 0."""
        
        self.board = [[0 for _ in range(4)] for _ in range(4)]