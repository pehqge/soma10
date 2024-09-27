from interface import Interface

class GameInterface(Interface):
    def __init__(self, main_controller, game_controller):
        super().__init__(main_controller)
        self.game_controller = game_controller
        self.main_controller = main_controller
        self.informacoes = {"j2_fichas": 0, "j2_pontos": 0, "j1_pontos": 0, "j1_fichas": [], "board": self.game_controller.board.board, "notifications": [], "shop_size": self.game_controller.deck.size}
        self.setup()
    
    def setup(self):
        # Carrega e exibe o background
        self.ui_tools.load_and_display("bg", "assets/jogo/fundo.png", 0, 0)
        
        # Exibe o tabuleiro   
        self.ui_tools.load_and_display("tabuleiro", "assets/jogo/tabuleiro.png", 392, 174)
        self.render_board(self.informacoes["board"])
        
        # Menu Jogador 1
        self.render_local_player(self.informacoes["j1_fichas"], self.informacoes["j1_pontos"])
        
        # Menu Jogador 2
        self.ui_tools.load_and_display("j2_card", "assets/jogo/jogador2.png", 900, 40)
        
        self.ui_tools.write_text(text=f'{self.informacoes["j2_fichas"]} fichas', x=1013, y=195, size=43, color="white", font="font_kid") # qntd de fichas do jogador 2
        self.ui_tools.write_text(text=f'{self.informacoes["j2_pontos"]} pontos', x=1028, y=92, size=34, color="white", font="font_kid") # qntd de pontos do jogador 2
        
        # Notificacoes do Jogo
        self.display_notification(self.informacoes["notifications"])
        
        # Loja de itens
        if self.informacoes["shop_size"] > 0:
            static = False
        else:
            static = True
        self.ui_tools.create_shop_button(self.informacoes["shop_size"], self.game_controller.buy_card, static)
        
        # Botao de voltar para o menu e resetar game
        self.ui_tools.create_resizable_button("assets/jogo/close.png", 1242, 40, self.show_menu)
        
    def show_menu(self):
        self.hide()
        self.main_controller.show_menu()
        
    def render_board(self, board):
        """ Renderiza o tabuleiro de jogo. """
        
        # Para cada célula do tabuleiro, renderiza uma célula
        for i in range(4):
            for j in range(4):
                on_click = lambda event, value1=i, value2=j: self.game_controller.put_card(value1, value2) # Função que será ativada quando a carta for clicada
                self.ui_tools.create_board_cell(card_number=board[i][j], i=i, j=j, on_click=on_click)
        
    def render_local_player(self, cards, points):
        """ Renderiza o menu do jogador local. """
        
        # Inicializa o card e a pontuacao do jogador 1
        self.ui_tools.load_and_display("j1_card", "assets/jogo/jogador1.png", 19, 42)
        self.ui_tools.write_text(text=f'{points} pontos', x=137, y=92, size=34, color="white", font="font_kid")
    
        # Renderiza as cartas do jogador 1
        for card_number in range(1,8):
            count = cards.count(card_number) # Quantidade daquela ficha no baralho do jogador

            if count > 0: # Se tiver mais de uma carta, a carta é clicável
                on_click = lambda event, value=card_number: self.game_controller.local_player.select_card(value) # Função que será ativada quando a carta for clicada
                
            else: # Se não tiver carta daquele número, ela não é clicável
                on_click = None

            # Cria a carta usando o UITools
            self.ui_tools.create_card(card_number=card_number, quantity=count, on_click=on_click)
        
    def display_notification(self, notifications):
        """ Exibe as notificações do jogo na tela do jogador. """
        
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
    
    def update(self, update_dict):
        for key, value in update_dict.items():
            self.informacoes[key] = value
        self.ui_tools.clear_canvas()
        self.setup()