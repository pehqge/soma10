from tkinter import Tk, Canvas, NW
from PIL import Image, ImageDraw, ImageTk, ImageFont
import random

class BoardGame:
    def __init__(self, game_frame):
        self.game_frame = game_frame
        
        # Configura o frame para o jogo
        self.game_frame.pack_forget()  # Começa escondido

        # Adicione os widgets do jogo aqui...
        self.canvas = Canvas(self.game_frame, width=1280, height=720)
        self.canvas.pack()
        
        # Inicia Background
        self.bg_image = ImageTk.PhotoImage(file="assets/jogo/fundo.png")
        self.canvas.create_image(0, 0, image=self.bg_image, anchor=NW)
        
        # Inicia o tabuleiro
        self.board_image = ImageTk.PhotoImage(file="assets/jogo/tabuleiro.png")
        self.canvas.create_image(392, 174, image=self.board_image, anchor=NW)
        self.board = [[0 for _ in range(4)] for _ in range(4)]
        
        for i in range(4):
            for j in range(4):
                self.create_cell(i, j) # cria cada bolinha do tabuleiro
                
        # Inicia jogador 1 e suas cartas
        self.selected_card = None # carta selecionada
        self.jogador_cartas = [] # começa o jogo com 3 cartas aleatorias
        self.j1_pontos = 27 # pontos do jogador 1
        self.create_card(self.jogador_cartas)
        
        # Inicia jogador 2
        self.jogador2_card = ImageTk.PhotoImage(file="assets/jogo/jogador2.png")
        self.canvas.create_image(900, 40, image=self.jogador2_card, anchor=NW)
        self.jogado2_bola = ImageTk.PhotoImage(file="assets/jogo/jogador2_bola.png")
        
        jogador2_cartas = 3 # Quantas cartas o jogador 2 possui atualmente
        self.canvas.create_image(977, 226, image=self.jogado2_bola, anchor=NW)
        self.write_text(f"{jogador2_cartas} cartas", x=1010, y=476, size=43, color="white", font="font_kid")
        
        j2_pontos = 27
        self.write_text(f"{j2_pontos} pontos", x=1023, y=92, size=34, color="white", font="font_kid")
        
        # Inicia Baralho de compras
        self.deck = [1] * 18 + [2] * 18 + [3] * 14 + [4] * 8 + [5] * 4 + [6] * 2 + [7] * 2 # Baralho de compras
        self.cartas_restantes = len(self.deck) # Quantas cartas restam no baralho
        self.shop_button()
        
        # Jogador inicia com 3 cartas
        for _ in range(3):
            self.buy_card()
        
        
    # Função para escrever um texto na tela
    def write_text(self, text, x, y, size, color, font):
        font = ImageFont.truetype(f"assets/jogo/{font}.ttf", size)
        image = Image.new("RGBA", (400, 100), (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), text, font=font, fill=color)
        
        text_image = ImageTk.PhotoImage(image)
        setattr(self, f"{font}_font", text_image)
        self.canvas.create_image(x, y, image=text_image, anchor=NW)
        
    # Função para criar um botão que anima quando passa o mouse
    def animated_button(self, image, x, y, inactive=False, shop=False):
        
        # Flag usada por cartas que não podem ser clicadas
        if inactive:
            image = f"{image}o"
        
        # Imagens para animação
        original_image = Image.open(f"assets/jogo/{image}.png")
        resized_image = original_image.resize(
            (int(original_image.width * 1.05), int(original_image.height * 1.05))
        )
        
        # Converte para o formato compatível com o Tkinter
        original_image_tk = ImageTk.PhotoImage(original_image)
        resized_image_tk = ImageTk.PhotoImage(resized_image)
        
        # Armazena as imagens na instância da classe
        setattr(self, f"{image}_original", original_image_tk)
        setattr(self, f"{image}_resized", resized_image_tk)
        
        # Cria o botão no Canvas com a imagem original
        button_id = self.canvas.create_image(x, y, image=original_image_tk, anchor=NW)
        
        # Vincula eventos de mouse
        if not inactive: # se for um botão normal
            self.canvas.tag_bind(button_id, "<Enter>", lambda event: self.move_button(event, button_id, resized_image_tk)) # quando passa ele aumenta
            self.canvas.tag_bind(button_id, "<Leave>", lambda event: self.move_button(event, button_id, original_image_tk)) # quando sai ele volta ao normal
            
            if shop: # se for o botão de comprar
                self.canvas.tag_bind(button_id, "<Button-1>", lambda event: self.buy_card())
                
            else: # se for uma carta
                self.canvas.tag_bind(button_id, "<Button-1>", lambda event: self.select_card(event, image))

    # Função para a animação do botão
    def move_button(self, event, button_id, new_image):
        self.canvas.itemconfig(button_id, image=new_image)
        
    # Função para criar uma célula do tabuleiro
    def create_cell(self, i, j):
        ball = ImageTk.PhotoImage(file="assets/jogo/bola.png")
        setattr(self, f"ball{i}{j}", ball)
    
        ball_id = self.canvas.create_image(392 + 124 * i, 174 + 124 * j, image=ball, anchor=NW)
        
        self.canvas.tag_bind(ball_id, "<Button-1>", lambda event: self.put_card(event, i, j)) # quando clica na bola
    
    # Função para colocar uma carta no tabuleiro
    def put_card(self, event, i, j):
        if self.selected_card:
            self.board[i][j] = int(self.selected_card)
            
            for x in range(4):
                for y in range(4):
                    print(self.board[y][x], end=" ")
                print()
            print()
            
            self.canvas.create_image(392 + 124 * i, 174 + 124 * j, image=getattr(self, f"{self.selected_card}_original"), anchor=NW)
            self.jogador_cartas.remove(int(self.selected_card))
            self.create_card(self.jogador_cartas)
            self.selected_card = None
            
            self.buy_card()
        
    # Função para criar uma carta na mesa do jogador
    def create_card(self, cards):
        self.cartas_pos = [(90, 173), (90, 285), (90, 397), (90, 509), (190, 230), (190, 342), (190, 454)] # Posições das cartas
        
        self.jogador1_card = ImageTk.PhotoImage(file="assets/jogo/jogador1.png")
        self.canvas.create_image(19, 42, image=self.jogador1_card, anchor=NW)
        
        self.write_text(f"{self.j1_pontos} pontos", x=137, y=92, size=34, color="white", font="font_kid")
        
        for i in range(1, 8):
            
            # Se tiver mais de uma carta, ele cria uma bolinha em cima falando quantas cartas
            if cards.count(i) > 1:
                self.animated_button(f"{i}", *self.cartas_pos[i-1])
                self.item = ImageTk.PhotoImage(file=f"assets/jogo/item.png")
                setattr(self, f"item_{i}", self.item)
                self.canvas.create_image(self.cartas_pos[i-1][0] + 45, self.cartas_pos[i-1][1]-20, image=self.item, anchor=NW, tags="card")
                self.write_text(f"{cards.count(i)}", self.cartas_pos[i-1][0] + 85, self.cartas_pos[i-1][1] + 16, 29, "#FF648D", "quicksand bold")
            
            # Se tiver uma carta, ele cria a carta
            elif cards.count(i) == 1:
                self.animated_button(f"{i}", *self.cartas_pos[i-1])
                
            # Se não tiver carta, ele cria uma carta inoperante
            else:
                self.animated_button(f"{i}", *self.cartas_pos[i-1], inactive=True)
    
    # Função para comprar uma carta    
    def buy_card(self):
        if self.cartas_restantes > 0:
            self.cartas_restantes -= 1
            self.shop_button()
            
            # Escolhe uma carta aleatória do baralho
            new_card = random.choice(self.deck)
            self.deck.remove(new_card)
                    
            # Adiciona a carta ao jogador 1
            self.jogador_cartas.append(new_card)
            
            self.j1_pontos += 1
            
            # Atualiza a exibição das cartas do jogador 1
            self.create_card(self.jogador_cartas)
        
    def select_card(self, event, card):
        self.selected_card = card
        
    def shop_button(self):
        self.compra_fundo = ImageTk.PhotoImage(file="assets/jogo/compra_fundo.png")
        self.canvas.create_image(530, 40, image=self.compra_fundo, anchor=NW)
        self.animated_button("compra", 450, 8, shop=True)
        self.write_text(f"{self.cartas_restantes} cartas restantes", x=604, y=80, size=18, color="#FF4D8D", font="quicksand")
        
        