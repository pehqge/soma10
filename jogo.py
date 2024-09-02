from tkinter import Tk, Canvas, NW
from PIL import Image, ImageDraw, ImageTk, ImageFont

class BoardGame:
    def __init__(self):
        # Inicia a tela
        self.mainWindow = Tk()
        self.mainWindow.title("Soma10")
        self.mainWindow.geometry("1280x720")
        self.mainWindow.resizable(False, False)
        self.canvas = Canvas(self.mainWindow, width=1280, height=720)
        self.canvas.pack()
        
        # Inicia Background
        self.bg_image = ImageTk.PhotoImage(file="assets/jogo/fundo.png")
        self.canvas.create_image(0, 0, image=self.bg_image, anchor=NW)
        
        # Inicia o tabuleiro
        self.board_image = ImageTk.PhotoImage(file="assets/jogo/tabuleiro.png")
        self.canvas.create_image(392, 174, image=self.board_image, anchor=NW)
        
        
    # def cell_generator(self):
        self.ball = ImageTk.PhotoImage(file="assets/jogo/bola.png")
        
        for i in range(4):
            for j in range(4):
                self.canvas.create_image(392 + 124 * i, 174 + 124 * j, image=self.ball, anchor=NW)
                
        # Inicia cards jogadores
        self.jogador1_card = ImageTk.PhotoImage(file="assets/jogo/jogador1.png")
        self.jogador2_card = ImageTk.PhotoImage(file="assets/jogo/jogador2.png")
        self.canvas.create_image(19, 42, image=self.jogador1_card, anchor=NW)
        self.canvas.create_image(900, 40, image=self.jogador2_card, anchor=NW)
        
        # Texto de jogadores
        j1_pontos = 34
        self.write_text("Jogador 1", x=145, y=65, size=26, color="white", font="font_kid")
        self.write_text(f"{j1_pontos} pontos", x=131, y=92, size=34, color="white", font="font_kid")
        
        j2_pontos = 27
        self.write_text("Jogador 2", x=1034, y=65, size=26, color="white", font="font_kid")
        self.write_text(f"{j2_pontos} pontos", x=1025, y=92, size=34, color="white", font="font_kid")
        
        # Inicia Baralho de compras
        self.compra_fundo = ImageTk.PhotoImage(file="assets/jogo/compra_fundo.png")
        self.canvas.create_image(540, 40, image=self.compra_fundo, anchor=NW)
        
        self.compra = ImageTk.PhotoImage(file="assets/jogo/compra.png")
        self.canvas.create_image(455, 8, image=self.compra, anchor=NW)
        
        cartas_restantes = 35
        self.write_text("baralho de compra", x=600, y=59, size=19, color="#FF4D8D", font="quicksand bold")
        self.write_text(f"{cartas_restantes} cartas restantes", x=600, y=80, size=18, color="#FF4D8D", font="quicksand")
        
        # Inicia o programa
        self.mainWindow.mainloop()
        
    def write_text(self, text, x, y, size, color, font):
        font = ImageFont.truetype(f"assets/jogo/{font}.ttf", size)
        image = Image.new("RGBA", (400, 100), (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), text, font=font, fill=color)
        
        text_image = ImageTk.PhotoImage(image)
        setattr(self, f"{font}_font", text_image)
        self.canvas.create_image(x, y, image=text_image, anchor=NW)
        
BoardGame()
        