from game_interface import GameInterface
from board import Board
from player import Player
from card_deck import CardDeck
from notification_manager import NotificationManager
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor

# Match Status
# 1 - Jogo não iniciado (Aguardando outro jogador)
# 2 - Jogo finalizado (Vitória ou derrota)
# 3 - Vez do jogador local
# 4 - Vez do jogador remoto (Aguardando ação do jogador remoto)
# 5 - Jogo abandonado (Desconexão de um dos jogadores)
# 6 - Erro


class GameController(DogPlayerInterface):
    def __init__(self, main_controller):
        self.main_controller = main_controller
        
        # Inicializa as classes
        self.board = Board()
        self.local_player = Player("Jogador 1", 1)
        self.remote_player = Player("Jogador 2", 2)
        self.deck = CardDeck()
        self.notification_manager = NotificationManager()
        self.interface = GameInterface(main_controller, self)
        
        # Inicializa o status da partida e o Dog
        self.match_status = 1
        self.dog_actor = DogActor()
        
        # Envia a lista de itens para a interface
        self.update_interface()
        
        
    def start_match(self):
        """Inicia a partida ao clicar em 'Iniciar Jogo'."""
        
        # Inicia a interface do jogo
        self.interface.show()
        self.interface.setup()
        
        self.notify("Aguardando o outro jogador se conectar ao jogo...")
        
        # Tenta fazer a conexão com o servidor
        self.request_connection()


    def request_connection(self):
        """Solicita ao servidor o início da partida. Fica em loop até que a conexão seja feita."""

        start_status = self.dog_actor.start_match(2)
        code = start_status.get_code()
        
        if code in ["0", "1"]: # erro de conexao ou jogadores insuficientes
            
            # Tenta novamente em 2 segundos se ainda não estiver conectado
            self.interface.root.after(2000, self.request_connection)
            
        else:
            
            # Se conectou, inicia o jogo
            self.initialize_game(start_status)
                

    def initialize_game(self, start_status):
        """Configura o jogo após ambos os jogadores estarem conectados."""
        
        # Recebe os jogadores do servidor e atualiza os dados
        players = start_status.get_players()
        local_id = start_status.get_local_id()
        
        local_info = self.get_local_player(players, local_id)
        remote_info = self.get_remote_player(players, local_id)
        
        self.local_player.update_info(local_info)
        self.remote_player.update_info(remote_info)
        
        # Exibe a notificação de início da partida
        self.notify(f"O jogador {remote_info[0]} se conectou ao jogo! Iniciando partida...")

        # Vez do jogador local 
        self.set_match_status(3) 
        self.local_player.turn = True
        self.notification_manager.notify_turn()
        
        # Inicia o baralho e embaralha as cartas
        self.deck.initialize_deck()
        
        # Compra 3 cartas para cada jogador
        for _ in range(3):
            local_card = self.deck.buy_card()
            self.local_player.add_card(local_card)
            remote_card = self.deck.buy_card()
            self.remote_player.add_card(remote_card)
        
        # Envia as cartas iniciais para o adversário
        self.send_move("dealing_initial_cards")
        
        self.update_interface()
    
    def receive_start(self, start_status):
        """Recebe a notificação do início da partida para o jogador que estava esperando."""
        
        # Tira o jogador do menu principal e exibe a interface do jogo
        self.interface.show()
        self.main_controller.main_menu.hide()
        
        # Vez do jogador remoto
        self.set_match_status(4)

        # Atualiza os dados dos jogadores vindos do servidor
        players = start_status.get_players()
        local_id = start_status.get_local_id()
        
        local_info = self.get_local_player(players, local_id)
        remote_info = self.get_remote_player(players, local_id)

        self.local_player.update_info(local_info)
        self.remote_player.update_info(remote_info)
        
        # Exibe a notificação de início da partida
        self.notify(f"O jogador {remote_info[0]} iniciou a partida!")
        
        self.update_interface()
    
    def send_move(self, move_nature):
        """Envia o movimento para o adversário."""
        
        # Dados do movimento
        move_data = {
            "nature": move_nature,
            "board": self.board.board,
            "deck": self.deck.deck,
            "local_hand": self.remote_player.cards,
            "remote_score": self.local_player.score,
            "match_status": "next"
        }
        
        # Envia o movimento pelo dog
        self.dog_actor.send_move(move_data)
                
    def receive_move(self, move_data: dict):
        """Recebe o movimento do adversário."""
        
        # Recebe a natureza que identifica qual tipo de movimento foi feito
        nature = move_data["nature"] 

        match nature:
            case "game_over":
                
                # Define jogo como encerrado
                self.set_match_status(2)
                
                # Verifica o vencedor e mostra
                winner = self.check_winner()
                self.interface.root.after(1000, lambda: self.interface.display_winner(winner))
                return
            
            case "normal_play":
                
                # Recebe os dados do movimento e os atualiza
                self.deck.update_deck(move_data["deck"])
                self.board.update_board(move_data["board"])
                remote_score = self.remote_player.score
                self.remote_player.update_score(move_data["remote_score"])
                
                # Se caso a pontuacao do jogador remoto for diferente, notifica ao usuario que ele pontuou
                if remote_score < self.remote_player.score:
                    self.notify(f"{self.remote_player.name} somou 10 e marcou {self.remote_player.score - remote_score} pontos!")
                
                
                # Verificacao de equidade de cartas
                cards = self.verify_card_equity()
                              
                for _ in range(cards):
                    self.buy_card("system")
                
                # Muda o turno para que seja vez do jogador local
                self.switch_turn()
                self.set_match_status(3)
                
                    
            case "buy_card":
                
                # Recebe o baralho atualizado
                self.deck.update_deck(move_data["deck"])
                
                # Verifica a equidade de cartas
                cards = self.verify_card_equity()
                
                for _ in range(cards):
                    self.buy_card("system")

                # Muda o turno para que seja vez do jogador local
                self.switch_turn()
                self.set_match_status(3)
                
                    
            case "dealing_initial_cards":
                
                # Recebe as cartas iniciais
                self.deck.update_deck(move_data["deck"])
                self.local_player.update_hand(move_data["local_hand"])
                self.local_player.update_card_number(len(self.local_player.cards))

        self.update_interface()

        
    def receive_withdrawal_notification(self):
        """Recebe a notificação de que o outro jogador saiu da partida."""
        
        # Define o status da partida como 5 (jogo abandonado)
        self.set_match_status(5)
        self.notify("O outro jogador saiu da partida. O jogo irá fechar em 5 segundos...")
        
        # Encerra a aplicação depois de 5 segundos (para dar tempo do usuário ler a mensagem)
        self.interface.root.after(5000, self.main_controller.exit)
        
    def choose_card(self, value):
        """Seleciona uma carta."""
        
        # Reseta o board (para nao sobrepor com a ultima carta escolhida)
        self.interface.render_board()
        
        # Atualiza a carta escolhida
        self.local_player.choose_card(value)
        
        # Verifica as jogadas disponíveis e bloqueia as posições inválidas
        available_moves = self.check_available_moves(value)
        available_matrix = self.convert_available_list_to_matrix(available_moves)
        
        for i in range(4):
            for j in range(4):
                if not available_matrix[i][j]:
                    self.interface.block_position(j, i)
                
    def put_card(self, i: int, j: int):
        """Coloca uma carta no tabuleiro."""
    
        chosen_card = self.local_player.chosen_card
        
        # Se há uma carta escolhida
        if chosen_card != None:
            
            # Coloca a carta no board e remove a carta da mão do jogador e da seleção
            self.board.put_card(chosen_card, i, j)
            self.local_player.remove_card(chosen_card)
            self.local_player.choose_card(None)
            
            # Verifica se o jogador fez uma soma 10 e notifica caso aconteça
            pontos = 0
            for i in range(10):
                line = self.board.get_line(i)
                
                if sum(line) == 10:
                    self.board.clear_line(i)
                    self.local_player.add_score(4)
                    pontos += 4
            
            if pontos > 0:
                self.notify(f"Você somou 10 e marcou {pontos} pontos!")
            
            # Compra uma carta para o jogador
            self.buy_card("system")
            
            # Muda o turno para o jogador remoto
            self.switch_turn()
            self.set_match_status(4)
            
            self.send_move("normal_play")
            self.update_interface()
        
                
    def buy_card(self, called: str = "player"):
        """Compra uma carta."""

        # Limpa a seleção da carta (para não deixar o player colocar uma carta depois de comprar)
        self.local_player.choose_card(None)

        if called == "player":
            player = self.get_player_turn()
            
            # Se o player clicou enquanto não era sua vez, não deixa comprar
            if player != self.local_player:
                return
            
            # Verifica se ainda há jogadas disponíveis
            cards = self.local_player.get_cards()
            
            for card in cards:
                availables = self.check_available_moves(card)
                availables_matrix = self.convert_available_list_to_matrix(availables)
                
                # Se tiver, não deixa ele comprar
                if any(True in row for row in availables_matrix):
                    self.notify("Ainda há jogadas disponíveis, não é possível comprar cartas.")
                    return
        
        empty = self.deck.is_empty()
        
        # Se o baralho ainda tiver carta, compra
        if not empty:
            card = self.deck.buy_card()
            self.local_player.add_card(card)
            
            if called == "player":
                
                # Troca o turno para o jogador remoto e envia o movimento de compra de carta
                self.switch_turn()
                self.set_match_status(4)
                self.send_move("buy_card")
                
            self.update_interface()
        
        else:
            
            # Se o baralho está vazio, começa o processo de verificação de game over
            self.notify("Baralho está vazio! Não é possível comprar cartas.")
            
            # Se foi o sistema que chamou, verificar se o jogador possui jogadas a se fazer
            if called == "system":
                
                cards = self.local_player.get_cards()
                
                for card in cards:
                    availables = self.check_available_moves(card)
                    availables_matrix = self.convert_available_list_to_matrix(availables)
                    
                    # Se tiver, não caracteriza game over e retorna
                    if any(True in row for row in availables_matrix):
                        self.update_interface()
                        return
            
            # Se não tiver jogadas disponíveis, encerra o jogo  
            self.set_match_status(2) # game over
            
            # mostra o vencedor
            winner = self.check_winner()
            self.interface.root.after(10, lambda: self.interface.display_winner(winner))
            
            # envia que o jogo encerrou para o jogador remoto
            self.send_move("game_over")
                
    def check_available_moves(self, value) -> list: 
        """Retorna quais são as jogadas disponíveis em uma lista de booleanos.
            0 <= index <= 3 : linhas.
            4 <= index <= 7 : colunas.
            8 : diagonal principal.
            9 : diagonal secundária.
        """
        
        # Se for uma carta vazia, não há jogadas disponíveis
        if value == None:
            return [False for _ in range(10)]
        
        lines = [True for _ in range(10)]
        
        for i in range(10):
            line = self.board.get_line(i)

            # para saber quantas cartas já foram colocadas
            cards_put = 4 - line.count(0)
            
            # Define verdadeiro ou falso dependendo das regras do jogo
            match cards_put:
                case 1: # 1 carta ja colocada
                    if sum(line) + value > 8:
                        lines[i] = False
                case 2: # 2 cartas ja colocadas
                    if sum(line) + value > 9:
                        lines[i] = False
                case 3: # 3 cartas ja colocadas
                    if sum(line) + value != 10:
                        lines[i] = False
        
        return lines
    
    def convert_available_list_to_matrix(self, available_moves: list) -> list:
        """Converte a lista de jogadas disponíveis em uma matriz (faz com que não tenha sobreposição)."""
        
        matrix = []
        
        # Cria uma matriz de 4x4 com valores booleanos (inicializa ela com False para as posicoes ja preenchidas)
        for i in range(4):
            row = []
            for j in range(4):
                row.append(self.board.board[i][j] == 0)
            matrix.append(row)
        
        # Percorre a lista de jogadas disponíveis e bloqueia as posições inválidas
        for i in range(10):
            if not available_moves[i]:
                if i < 4: # linha
                    matrix[i] = [False, False, False, False]
                elif i < 8: # coluna
                    for j in range(4):
                        matrix[j][i-4] = False
                elif i == 8: # diagonal principal
                    for j in range(4):
                        matrix[j][j] = False
                else: # diagonal secundária
                    for j in range(4):
                        matrix[j][3-j] = False
        
        return matrix
    
    def verify_card_equity(self):
        """Verifica quantas cartas de diferença entre os jogadores."""
        
        local_cards = self.local_player.card_number
        remote_cards = self.remote_player.card_number
        
        if remote_cards > local_cards:
            return remote_cards - local_cards
        
        return 0
    
    def check_winner(self):
        """Retorna se o jogador local venceu. (empate conta como vitória)"""
        
        if self.local_player.score >= self.remote_player.score:
            self.local_player.attribute_victory()
            return True
        else:
            self.remote_player.attribute_victory()
            return False
        
    def switch_turn(self):
        """Troca a vez dos jogadores."""
        
        # Se for a vez do jogador local, passa para o remoto e remove a notificação de turno
        if self.local_player.turn:
            self.local_player.turn = False
            self.remote_player.turn = True
            self.notification_manager.remove_turn_notification()
            
        else: # Se for a vez do jogador remoto, passa para o local e notifica que é seu turno
            self.local_player.turn = True
            self.remote_player.turn = False
            self.notification_manager.notify_turn()

    def notify(self, message: str):
        """Notifica o jogador."""
        
        self.notification_manager.add_notification(message)
        self.update_interface()
    
    def update_interface(self):
        """Atualiza a interface do jogo com os dados atuais da jogada."""
        
        # Informações que serão enviadas para a interface
        informations = {
            "j2_pontos": self.remote_player.score,
            "j1_pontos": self.local_player.score,
            "j1_fichas": self.local_player.cards,
            "shop_size": len(self.deck.deck),
            "board": self.board.board,
            "notifications": self.notification_manager.notifications,
            "aguardando": self.match_status == 4
        }
        
        # Só atualiza a interface se ela existir e o jogo não tiver acabado
        match_status = self.get_match_status()
        
        if self.interface.root and self.interface.root.winfo_exists() and match_status != 2:
            self.interface.root.after(0, lambda: self.interface.update(informations))
            
    
    def get_local_player(self, players, local_id):
        """Retorna o jogador local."""
        
        for player in players:
            if player[1] == local_id:
                return player
        return player
    
    def get_remote_player(self, players, local_id):
        """Retorna o jogador remoto."""
        
        for player in players:
            if player[1] != local_id:
                return player
        return player
        
    def get_player_turn(self):
        """Retorna o jogador da vez."""
        
        if self.local_player.turn:
            return self.local_player
        else:
            return self.remote_player
            
    def get_match_status(self):
        """Retorna o status da partida."""
        
        return self.match_status   
    
    def set_match_status(self, status: int):
        """Define o status da partida."""
        
        self.match_status = status
