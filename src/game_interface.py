from interface import Interface

from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor
from tkinter import messagebox  # para conexão com dog
from tkinter import simpledialog  # para conexão com dog

class GameInterface(Interface, DogPlayerInterface):
    def __init__(self, main_controller, game_controller):
        super().__init__(main_controller)
        self.game_controller = game_controller
        
        # conexão com o dog
        player_name = simpledialog.askstring(title="Player identification", prompt="Qual o seu nome?")
        self.dog_server_interface = DogActor()
        message = self.dog_server_interface.initialize(player_name, self)
        messagebox.showinfo(message=message)

    def setup(self):
        # Carrega e exibe o background
        self.ui_tools.load_and_display("bg", "assets/jogo/fundo.png", 0, 0)
        
        # Exibe o tabuleiro   
        self.ui_tools.load_and_display("tabuleiro", "assets/jogo/tabuleiro.png", 392, 174)
        self.render_board()
        
        # Menu Jogador 1
        self.render_local_player()
        
        # Menu Jogador 2
        self.ui_tools.load_and_display("j2_card", "assets/jogo/jogador2.png", 900, 40)
        
        self.ui_tools.write_text(text=f'{self.informacoes["j2_fichas"]} fichas', x=1013, y=195, size=43, color="white", font="font_kid") # qntd de fichas do jogador 2
        self.ui_tools.write_text(text=f'{self.informacoes["j2_pontos"]} pontos', x=1028, y=92, size=34, color="white", font="font_kid") # qntd de pontos do jogador 2
        
        # Notificacoes do Jogo
        self.display_notification()
        
        # Loja de itens
        if self.informacoes["shop_size"] > 0: # Se a loja não estiver vazia, o botão é clicável
            static = False # Flag que indica se o botão é clicável
        else:
            static = True
        self.ui_tools.create_shop_button(self.informacoes["shop_size"], self.game_controller.buy_card, static)
        
        # Botao de voltar para o menu e resetar game
        self.ui_tools.create_resizable_button("assets/jogo/close.png", 1242, 40, self.main_controller.show_menu)
        
    def render_board(self):
        """ Renderiza o tabuleiro de jogo. """
        
        board = self.informacoes["board"] # recebe o estado atual do board do jogo
        
        # Para cada célula do tabuleiro, renderiza uma célula
        for i in range(4):
            for j in range(4):
                on_click = lambda event, value1=i, value2=j: self.game_controller.put_card(value1, value2) # Função que será ativada quando a carta for clicada
                self.ui_tools.create_board_cell(card_number=board[i][j], i=i, j=j, on_click=on_click)
        
    def render_local_player(self):
        """ Renderiza o menu do jogador local. """
        
        cards = self.informacoes["j1_fichas"] # Fichas do jogador 1
        points = self.informacoes["j1_pontos"] # Pontuação do jogador 1
        
        # Inicializa o card e a pontuacao do jogador 1
        self.ui_tools.load_and_display("j1_card", "assets/jogo/jogador1.png", 19, 42)
        self.ui_tools.write_text(text=f'{points} pontos', x=137, y=92, size=34, color="white", font="font_kid")
    
        # Renderiza as fichas que o jogador 1 tem em mão
        for card_number in range(1,8):
            count = cards.count(card_number) # Quantidade daquela ficha no baralho do jogador

            if count > 0: # Se tiver pelo menos uma carta, a carta é clicável
                on_click = lambda event, value=card_number: self.game_controller.local_player.select_card(value) # Função que será ativada quando a carta for clicada
                
            else: # Se não tiver carta daquele número, ela não é clicável
                on_click = None

            # Cria a carta usando o UITools
            self.ui_tools.create_card(card_number=card_number, quantity=count, on_click=on_click)
        
    def display_notification(self):
        """ Exibe as notificações do jogo na tela do jogador. """
        
        notifications = self.informacoes["notifications"]
        
        self.ui_tools.load_and_display("notification", "assets/jogo/notification.png", 906, 277) # Exibe o background das notificações
        
        # Posição inicial das notificações
        x = 960
        y = 393
        
        for idx, notification in enumerate(notifications):
            if idx == 0: # Se for a primeira notificação, a cor é mais forte
                color = "#F70F6D"
            else:
                color = "#f6a7be"
                
            # Escreve o texto da notificação
            self.ui_tools.write_text(text=notification, x=x, y=y, size=24, color=color, font="font_kid")
            y += 24 # Incrementa a posição Y para a próxima notificação
    
    def update(self, update_dict: dict):
        """ Atualiza as informações do jogo vindas do controller. """
        
        self.informacoes = update_dict # Atualiza as informações do jogo
        
        # Reseta a interface
        self.ui_tools.clear_canvas()
        self.setup()

    def start_match(self):
        start_status = self.dog_server_interface.start_match(2) # invoca o método do DOG e indica a quantidade de jogadores
        message = start_status.get_message()
        messagebox.showinfo(message=message)

    def receive_start(self, start_status):
        message = start_status.get_message()
        messagebox.showinfo(message=message)
