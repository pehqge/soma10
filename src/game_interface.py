from tkinter import Frame, Canvas, NW
from PIL import Image, ImageTk
from game_controller import GameController

class GameInterface:
    def __init__(self, frame: Frame, controller: GameController):
        self.__frame = frame
        self.__controller = controller
        self.__images = {"bg": "assets/jogo/fundo.png", "board_grid": "assets/jogo/tabuleiro.png"}
    
    def initialize(self):
        # Inicializa a interface do jogo
        self.__game_frame.pack_forget()
        self.__canvas = Canvas(self.__frame, width=1280, height=720)
        self.__canvas.pack()
        
        # Carrega a imagem de fundo
        self.load_background()
        
        # Renderiza o tabuleiro
        board_grid = ImageTk.PhotoImage(file=self.__images["board_grid"])
        self.__canvas.create_image(392, 174, image=board_grid, anchor=NW)
        
    def load_background(self):
        bg_image = ImageTk.PhotoImage(file=self.__images["bg"])
        self.__canvas.create_image(0, 0, image=bg_image, anchor=NW)
        
    def render_board(self):
        board = self.__controller.board.board
        
        for row in range(4):
            for col in range(4):
                card = board[row][col]
                card_image = card.image
                self.__canvas.create_image(100 + 200 * col, 100 + 200 * row, image=card_image, anchor=NW)