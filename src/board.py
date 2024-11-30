class Board:
    def __init__(self):
        # Inicializa o board 4x4 vazio
        self.board = [[0 for _ in range(4)] for _ in range(4)]
        
    def update_board(self, board):
        """Atualiza o tabuleiro."""
        
        self.board = board
        
    def get_line(self, i: int):
        """ Retorna a reta i do tabuleiro.
            0 <= i <= 3 : Retorna a linha i.
            4 <= i <= 7 : Retorna a coluna i-4.
            8 : Retorna a diagonal principal.
            9 : Retorna a diagonal secundária. 
        """
        
        if i < 4:
            return self.board[i]
        elif i < 8:
            return [self.board[j][i-4] for j in range(4)]
        elif i == 8:
            return [self.board[j][j] for j in range(4)]
        else:
            return [self.board[j][3-j] for j in range(4)]
    
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