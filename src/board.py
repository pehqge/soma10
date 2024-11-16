class Board:
    def __init__(self):
        # Inicializa o board 4x4 vazio
        self.board = [[0 for _ in range(4)] for _ in range(4)]
    
    def put_card(self, card_number: int, i: int, j: int):
        """Coloca uma carta no tabuleiro."""
        
        self.board[i][j] = card_number
        
    def remove(self, type: str, i: int):
        """Remove uma linha, coluna ou diagonal do tabuleiro."""
        
        if type == "row": # Remove uma linha
            self.board[i] = [0, 0, 0, 0]
            
        elif type == "column": # Remove uma coluna
            for row in self.board:
                row[i] = 0
                
        elif type == "1_diagonal": # Remove a diagonal principal
            for i in range(4):
                self.board[i][i] = 0
        
        elif type == "2_diagonal": # Remove a diagonal secundária
            for i in range(4):
                self.board[i][3-i] = 0
                
        else:
            raise ValueError("Invalid type")

    def reset(self):
        """Reinicia o tabuleiro voltando tudo para 0."""
        
        self.board = [[0 for _ in range(4)] for _ in range(4)]