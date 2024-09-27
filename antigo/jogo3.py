from tkinter import Canvas, NW
from PIL import Image, ImageDraw, ImageTk, ImageFont
import random

class BoardGame:
    def __init__(self, game_frame):
        self.game_frame = game_frame
        
        # Configura o frame para o jogo
        self.game_frame.pack_forget()  
        self.canvas = Canvas(self.game_frame, width=1280, height=720)
        self.canvas.pack()
        
        # Inicia Background
        self.bg_image = ImageTk.PhotoImage(file="assets/jogo/fundo.png")
        self.canvas.create_image(0, 0, image=self.bg_image, anchor=NW)
        
        # Inicia o tabuleiro
        self.board_image = ImageTk.PhotoImage(file="assets/jogo/tabuleiro.png")
        self.canvas.create_image(392, 174, image=self.board_image, anchor=NW)
        self.board = [[0 for _ in range(4)] for _ in range(4)] # matriz para armazenar as fichas que estão no tabuleiro
        
        # Inicia as bolinhas do tabuleiro
        self.render_board()
                
        # Inicia jogador 1 e suas fichas
        self.selected_card = None # ficha selecionada pelo jogador
        self.jogador_fichas = [] # fichas do jogador
        self.j1_pontos = 0 # pontos do jogador 1
        self.create_cards(self.jogador_fichas)
        
        # Inicia jogador 2
        self.jogador2_card = ImageTk.PhotoImage(file="assets/jogo/jogador2.png")
        self.canvas.create_image(900, 40, image=self.jogador2_card, anchor=NW)
        self.jogado2_bola = ImageTk.PhotoImage(file="assets/jogo/jogador2_bola.png")
        
        jogador2_fichas = 3 # Quantas fichas o jogador 2 possui atualmente
        self.canvas.create_image(977, 226, image=self.jogado2_bola, anchor=NW)
        self.write_text(f"{jogador2_fichas} fichas", x=1010, y=476, size=43, color="white", font="font_kid")
        
        j2_pontos = 27
        self.write_text(f"{j2_pontos} pontos", x=1023, y=92, size=34, color="white", font="font_kid")
        
        # Inicia Baralho de compras
        self.deck = [1] * 18 + [2] * 18 + [3] * 14 + [4] * 8 + [5] * 4 + [6] * 2 + [7] * 2 # Baralho de compras
        self.fichas_restantes = len(self.deck) # Quantas fichas restam no baralho
        self.shop_button()
        
        # Jogador inicia com 3 fichas
        for _ in range(3):
            self.buy_card()
            
    def check_sum10(self):
        # checks if any row or colum or diagonal has sum 10
        for i in range(4):
            if sum(self.board[i]) >= 10:
                return (True, [(i, j) for j in range(4)])
            if sum([self.board[j][i] for j in range(4)]) >= 10:
                return (True, [(j, i) for j in range(4)])
            if sum([self.board[i][i] for i in range(4)]) >= 10:
                return (True, [(i, i) for i in range(4)])
            if sum([self.board[i][3-i] for i in range(4)]) >= 10:
                return (True, [(i, 3-i) for i in range(4)])
        return (False, [])
        
    def render_board(self, card=None):
        if card:
            print(f"Selecionou a ficha {card}")
            valid_positions = self.valid_moves(card)  # Obtém as posições válidas
            
            for i in range(4):
                for j in range(4):
                    self.blank_cell(i, j)  # Limpa a célula

                    if self.board[i][j] != 0:
                        # Renderiza a ficha normal
                        self.canvas.create_image(392 + 124 * i, 174 + 124 * j, image=getattr(self, f"{self.board[i][j]}_original"), anchor=NW)
                    elif (i, j) not in valid_positions:
                        # Escurece as células inválidas
                        self.dark_cell(i, j)
        else:
            for i in range(4):
                for j in range(4):
                    self.blank_cell(i, j)  # Apaga a célula
                    if self.board[i][j] != 0:
                        # Renderiza a ficha normal
                        self.canvas.create_image(392 + 124 * i, 174 + 124 * j, image=getattr(self, f"{self.board[i][j]}_original"), anchor=NW)
        
        # Verifica o check_sum10
        if self.check_sum10()[0]:
            # Coleta as posições que precisam ser escurecidas
            positions_to_clear = self.check_sum10()[1]

            # Escurece as fichas
            for i, j in positions_to_clear:
                self.white_cell(i, j)  # Função que cria a célula escurecida

            # Aguardar 1 segundo antes de apagar as fichas
            self.canvas.after(1000, lambda: self.clear_cells(positions_to_clear))
            
    def valid_moves(self, card):
        """Retorna uma lista de posições válidas para colocar a carta."""
        valid_positions = []
        card_value = int(card)  # Converte a carta selecionada para um valor numérico

        for i in range(4):
            for j in range(4):
                # Verifica se a célula está vazia
                if self.board[i][j] == 0:
                    # Verifica as regras da fileira
                    if self.is_valid_in_row(i, j, card_value) and self.is_valid_in_column(i, j, card_value):
                        valid_positions.append((i, j))

        return valid_positions

    def is_valid_in_row(self, i, j, card_value):
        """Verifica se colocar a carta na linha `i` e coluna `j` é válido com base nas regras da fileira."""
        row_values = [self.board[i][col] for col in range(4) if self.board[i][col] != 0]
        if len(row_values) == 0:  # Primeiro cartão pode ser colocado em qualquer posição vazia
            return True
        elif len(row_values) == 1:  # Verifica se a soma das duas primeiras cartas é <= 8
            return (row_values[0] + card_value) <= 8
        elif len(row_values) == 2:  # Verifica se a soma das três primeiras cartas é <= 9
            return (row_values[0] + row_values[1] + card_value) <= 9
        elif len(row_values) == 3:  # Verifica se a soma das quatro cartas é exatamente 10
            return (row_values[0] + row_values[1] + row_values[2] + card_value) == 10
        return False

    def is_valid_in_column(self, i, j, card_value):
        """Verifica se colocar a carta na linha `i` e coluna `j` é válido com base nas regras da coluna."""
        column_values = [self.board[row][j] for row in range(4) if self.board[row][j] != 0]
        if len(column_values) == 0:  # Primeiro cartão pode ser colocado em qualquer posição vazia
            return True
        elif len(column_values) == 1:  # Verifica se a soma das duas primeiras cartas é <= 8
            return (column_values[0] + card_value) <= 8
        elif len(column_values) == 2:  # Verifica se a soma das três primeiras cartas é <= 9
            return (column_values[0] + column_values[1] + card_value) <= 9
        elif len(column_values) == 3:  # Verifica se a soma das quatro cartas é exatamente 10
            return (column_values[0] + column_values[1] + column_values[2] + card_value) == 10
        return False

    def dark_cell(self, i, j):
        # Carrega a versão escurecida da imagem
        dark_image = getattr(self, f"{self.board[i][j]}_dark", None)
        if not dark_image:
            original_image = Image.open(f"assets/jogo/{self.board[i][j]}.png")
            dark_image = original_image.point(lambda p: p * 0.5)  # Reduz o brilho da imagem
            dark_image = ImageTk.PhotoImage(dark_image)
            setattr(self, f"{self.board[i][j]}_dark", dark_image)  # Salva como atributo para uso futuro

        # Renderiza a imagem escurecida no canvas
        self.canvas.create_image(392 + 124 * i, 174 + 124 * j, image=dark_image, anchor=NW)
        
    def white_cell(self, i, j):
        # Carrega a versão clara da imagem
        white_image = getattr(self, f"{self.board[i][j]}_white", None)
        if not white_image:
            original_image = Image.open(f"assets/jogo/{self.board[i][j]}.png")
            white_image = original_image.point(lambda p: p * 1.3)
            white_image = ImageTk.PhotoImage(white_image)
            setattr(self, f"{self.board[i][j]}_white", white_image)
            
        # Renderiza a imagem clara no canvas
        self.canvas.create_image(392 + 124 * i, 174 + 124 * j, image=white_image, anchor=NW)

    def clear_cells(self, positions_to_clear):
        # Apaga as células no tabuleiro e atualiza a pontuação
        for i, j in positions_to_clear:
            self.board[i][j] = 0  # Limpa o valor da célula
        self.j1_pontos += 4  # Atualiza a pontuação
        self.render_board()  # Re-renderiza o tabuleiro
                    
    
    
    def write_text(self, text, x, y, size, color, font, more=False):
        ''' Função para escrever um texto na tela'''
        
        ix = 400
        iy = 100
        tx = 0
        ty = 0
        
        if more:
            tx = 90
            ty = 14
            ix = 123
            iy = 123
        
        font = ImageFont.truetype(f"assets/jogo/{font}.ttf", size)
        image = Image.new("RGBA", (ix, iy), (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        draw.text((tx, ty), text, font=font, fill=color)
        
        if more:
            return image
        
        text_image = ImageTk.PhotoImage(image)
        setattr(self, f"{font}_font", text_image)
        self.canvas.create_image(x, y, image=text_image, anchor=NW)
        
    def animated_button(self, image, x, y, inactive=False, shop=False, imagefont=None):
        ''' Função para criar um botão que anima quando passa o mouse'''
        
        # Flag usada por fichas com mais de uma unidade
        if imagefont != None:
            image = f"{image}p"
            original_image = Image.alpha_composite(Image.open(f"assets/jogo/{image}.png"), imagefont)
        else:
            # Flag usada por fichas que não podem ser clicadas
            if inactive:
                image = f"{image}o"
                
            original_image = Image.open(f"assets/jogo/{image}.png")
        

        # Imagens para animação
        # original_image = Image.open(f"assets/jogo/{image}.png")
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
                
            else: # se for uma ficha
                self.canvas.tag_bind(button_id, "<Button-1>", lambda event: self.select_card(event, image))

    def move_button(self, event, button_id, new_image):
        ''' Função para animar o botão quando passa o mouse'''
        
        self.canvas.itemconfig(button_id, image=new_image)


    def blank_cell(self, i, j):
        ''' Função para criar uma célula do tabuleiro'''
        
        ball = ImageTk.PhotoImage(file="assets/jogo/0.png")
        setattr(self, f"ball{i}{j}", ball)
    
        ball_id = self.canvas.create_image(392 + 124 * i, 174 + 124 * j, image=ball, anchor=NW)
        
        self.canvas.tag_bind(ball_id, "<Button-1>", lambda event: self.put_card(event, i, j)) # quando clica na bola
    

    def put_card(self, event, i, j):
        ''' Função para colocar uma ficha no tabuleiro'''
        
        if self.selected_card:
            self.board[i][j] = int(self.selected_card)
            
            for x in range(4):
                for y in range(4):
                    print(self.board[y][x], end=" ")
                print()
            print()
            
            self.render_board()
            self.jogador_fichas.remove(int(self.selected_card))
            self.create_cards(self.jogador_fichas)
            self.selected_card = None
            
            self.buy_card()
        
    def create_cards(self, cards):
        ''' Função para criar as fichas do jogador 1 e coloca-las na tela'''
        
        self.fichas_pos = [(90, 173), (90, 285), (90, 397), (90, 509), (190, 230), (190, 342), (190, 454)] # Posições das fichas
        
        self.jogador1_card = ImageTk.PhotoImage(file="assets/jogo/jogador1.png")
        self.canvas.create_image(19, 42, image=self.jogador1_card, anchor=NW)
        
        self.write_text(f"{self.j1_pontos} pontos", x=137, y=92, size=34, color="white", font="font_kid")
        
        for i in range(1, 8):
            
            # Se tiver mais de uma ficha, ele cria uma bolinha em cima falando quantas fichas
            if cards.count(i) > 1:
                imagefont = self.write_text(f"{cards.count(i)}", self.fichas_pos[i-1][0] + 90, self.fichas_pos[i-1][1] + 12, 29, "#FF648D", "quicksand bold", more=True)
                self.animated_button(f"{i}", *self.fichas_pos[i-1], imagefont=imagefont)
                # self.canvas.create_image(self.fichas_pos[i-1][0] + 45, self.fichas_pos[i-1][1]-20, image=self.item, anchor=NW, tags="card")
            
            # Se tiver uma ficha, ele cria a ficha
            elif cards.count(i) == 1:
                self.animated_button(f"{i}", *self.fichas_pos[i-1])
                
            # Se não tiver ficha, ele cria uma ficha inoperante
            else:
                self.animated_button(f"{i}", *self.fichas_pos[i-1], inactive=True)
    
     
    def buy_card(self):
        ''' Função para comprar uma ficha nova'''
        
        if self.fichas_restantes > 0:
            self.fichas_restantes -= 1
            self.shop_button()
            
            # Escolhe uma ficha aleatória do baralho
            new_card = random.choice(self.deck)
            self.deck.remove(new_card)
                    
            # Adiciona a ficha ao jogador 1
            self.jogador_fichas.append(new_card)
            
            # self.j1_pontos += 1
            
            # Atualiza a exibição das fichas do jogador 1
            self.create_cards(self.jogador_fichas)

        
    def select_card(self, event, card):
        ''' Função para o jogador selecionar uma ficha'''
        card = card.replace("p", "") # remove o "p" do nome da ficha caso seja com mais de uma ficha
        
        self.selected_card = card
        self.render_board(card)
        
    def shop_button(self):
        ''' Função para criar o botão de comprar fichas'''
        
        self.compra_fundo = ImageTk.PhotoImage(file="assets/jogo/compra_fundo.png")
        self.canvas.create_image(530, 40, image=self.compra_fundo, anchor=NW)
        self.animated_button("compra", 450, 8, shop=True)
        self.write_text(f"{self.fichas_restantes} fichas restantes", x=604, y=80, size=18, color="#FF4D8D", font="quicksand")
        
        