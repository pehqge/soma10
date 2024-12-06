from interface import Interface

class GameInterface(Interface):
    def __init__(self, main_controller, game_controller):
        super().__init__(main_controller)
        self.game_controller = game_controller
    
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
        
        self.ui_tools.write_text(text=f'{self.informacoes["j2_pontos"]} pontos', x=1023, y=132, size=34, color="white", font="font_kid") # qntd de pontos do jogador 2
        
        # Loja de itens
        self.ui_tools.create_shop_button(self.informacoes["shop_size"], self.game_controller.buy_card)
        
        # Tela de aguardando
        if self.informacoes["aguardando"]:
            self.ui_tools.load_and_display("aguardando", "assets/jogo/aguardando.png", 0, 0)
            
        # Notificacoes do Jogo
        self.display_notification()
            
        
    def render_board(self):
        """ Renderiza o tabuleiro de jogo. """
        
        board = self.informacoes["board"] # recebe o estado atual do board do jogo
        
        # Para cada célula do tabuleiro, renderiza uma célula
        for i in range(4):
            for j in range(4):
                on_click = (lambda event, value1=i, value2=j: 
                    self.game_controller.put_card(value2, value1))
                
                self.ui_tools.create_board_cell(card_number=board[j][i], i=i, j=j, on_click=on_click)
                
                    
    def block_position(self, i, j):
        """ Bloqueia a posição (i, j) do tabuleiro. """
    
        board = self.informacoes["board"]
        
        self.ui_tools.dark_cell(card_number=board[j][i], i=i, j=j)
        
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
                on_click = lambda event, value=card_number: self.game_controller.choose_card(value) # Função que será ativada quando a carta for clicada
                
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
                
            # Se a notificação for muito grande, quebra ela em várias linhas
            if len(notification) > 20:
                split = notification.split(" ")
                notification = ""
                
                tam_linha = 0
                for i in range(len(split)):
                    if tam_linha > 20:
                        notification += "\n"
                        tam_linha = 0
                        
                    notification += split[i] + " "
                    tam_linha += len(split[i]) + 1
            
            # Se a notificação for muito grande para caber na tela, para de exibir
            if y + notification.count("\n") * 24 > 610:
                break    
            
            # Escreve o texto da notificação
            self.ui_tools.write_text(text=notification, x=x, y=y, size=24, color=color, font="kg font")
            
            if "\n" in notification:
                y += notification.count("\n") * 24
            y += 24 # Incrementa a posição Y para a próxima notificação
            
    def display_winner(self, local_win: bool):
        """ Exibe a tela de vitória/derrota. """
        
        # limpa o display
        self.ui_tools.clear_canvas()
        
        self.ui_tools.load_and_display("bg gameover", "assets/jogo/fundo gameover.png", 0, 0) # Carrega o background
        self.ui_tools.create_resizable_button("assets/jogo/botao menu.png", 640, 630, self.main_controller.exit) # Botão de encerrar jogo
        
        # renderiza a pontuação de cada jogador
        j2_textoX = 825 - (len(str(self.informacoes["j2_pontos"])) - 1) * 18
        
        self.ui_tools.write_text(text=f'{self.informacoes["j1_pontos"]} pontos', x=316, y=466, size=34, color="#FF648D", font="quicksand")
        self.ui_tools.write_text(text=f'{self.informacoes["j2_pontos"]} pontos', x=j2_textoX, y=466, size=34, color="#FF648D", font="quicksand")
        
        
        # anuncio do vencedor
        if local_win:
            self.ui_tools.write_text("Você é o vencedor!!", 348, 260, 64, "#F7AA00", "quicksand", 1000)
        else:
            self.ui_tools.write_text("Você perdeu! :(", 420, 260, 64, "#FF648D", "quicksand", 1000)
            
        # posicao da coroa
        coroaX = 216
        if not local_win:
            coroaX = 1045
            
        self.ui_tools.load_and_display("coroa", "assets/jogo/coroa.png", coroaX, 360)
    
    def update(self, update_dict: dict):
        """ Atualiza as informações do jogo vindas do controller. """
        
        self.informacoes = update_dict # Atualiza as informações do jogo
        # Reseta a interface
        self.root.after(0, self.ui_tools.clear_canvas)
        self.root.after(0, self.setup)
        