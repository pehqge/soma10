class Board:
    def __init__(self):
        self.board = [[0 for _ in range(4)] for _ in range(4)]
    
    def put_card(self, card_number, i, j):
        self.board[i][j] = card_number
        
    def remove(self, type, i):
        if type == "row":
            self.board[i] = [0, 0, 0, 0]
            
        elif type == "column":
            for row in self.board:
                row[i] = 0
                
        elif type == "1_diagonal":
            for i in range(4):
                self.board[i][i] = 0
        
        elif type == "2_diagonal":
            for i in range(4):
                self.board[i][3-i] = 0
                
        else:
            raise ValueError("Invalid type")

    def reset_board(self):
        self.board = [[0 for _ in range(4)] for _ in range(4)]