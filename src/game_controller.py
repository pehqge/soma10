from game_interface import GameInterface
from board import Board
from player import Player
from card_deck import CardDeck
from notification_manager import NotificationManager
from dog.dog_interface import DogPlayerInterface
from tkinter import messagebox
from tkinter import simpledialog
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
        self.deck = CardDeck()
        self.notification_manager = NotificationManager()
        self.local_player = Player("Jogador 1", 1)
        self.remote_player = Player("Jogador 2", 2)
        self.interface = GameInterface(main_controller, self)
        
        self.match_status = 1
        self.dog_actor = DogActor()
        
        self.update_interface()
        
        
    def debug_start(self):
        """Inicia o jogo em modo de depuração."""
        self.interface.show()
        self.interface.setup()
        
        self.match_status = 3
        self.local_player.update_info(["Jogador 1", 1])
        self.local_player.turn = True
        self.debug = True
        
        self.deck.initialize_deck()
        
        for _ in range(3):
            self.local_player.add_card(self.deck.buy_card())
            self.remote_player.add_card(self.deck.buy_card())
            
        self.update_interface()
        
    def switch_turn(self):
        if self.local_player.turn:
            self.local_player.turn = False
            self.remote_player.turn = True
        else:
            self.local_player.turn = True
            self.remote_player.turn = False
        
    def start_match(self):
        """Inicia a partida ao clicar em 'Iniciar Jogo'."""
        self.interface.show()
        self.interface.setup()

        # Inicializa o DogActor
        player_name = simpledialog.askstring(title="Player identification", prompt="Qual o seu nome?")
        message = self.dog_actor.initialize(player_name, self)
        self.notify(message)
        
        if message == "Você está sem conexão":
            self.main_controller.show_menu()
        
        self.notify("Conectando ao servidor...")
        
        self.request_connection()


    def request_connection(self):
        """Solicita ao servidor o início da partida."""

        if self.match_status == 1:
            start_status = self.dog_actor.start_match(2)
            code = start_status.get_code()
            
            if code in ["0", "1"] and self.match_status == 1:
                # Exibe notificação informando que está tentando conectar
                self.notify("Aguardando outro jogador...")
                
                # Tenta novamente em 2 segundos se ainda não estiver conectado
                self.interface.root.after(2000, self.request_connection)
                
            else:
                self.notify("Jogador encontrado! Partida iniciando...")
                self.initialize_game(start_status)

    def initialize_game(self, start_status):
        """Configura o jogo após ambos os jogadores estarem conectados."""
        print("Partida iniciada!")

        self.reset_game()
        
        players = start_status.get_players()
        local_id = start_status.get_local_id()
        
        local_info = self.get_local_player(players, local_id)
        remote_info = self.get_remote_player(players, local_id)
        
        self.local_player.update_info(local_info)
        self.remote_player.update_info(remote_info)

        self.set_match_status(3)  # Vez do jogador local 
        self.local_player.turn = True
        
        # Inicia o baralho e distribui as cartas
        self.deck.initialize_deck()
        
        for _ in range(3):
            self.local_player.add_card(self.deck.buy_card())
            self.remote_player.add_card(self.deck.buy_card())
        
        self.send_move("dealing_initial_cards")
        
        self.notify("Partida iniciada!")
        self.update_interface()
    
    def receive_start(self, start_status):
        """Recebe a notificação do início da partida para o jogador que estava esperando."""
        print("Partida recebida!")

        self.reset_game()
        
        self.set_match_status(4)

        players = start_status.get_players()
        local_id = start_status.get_local_id()
        
        local_info = self.get_local_player(players, local_id)
        remote_info = self.get_remote_player(players, local_id)

        self.local_player.update_info(local_info)
        self.remote_player.update_info(remote_info)
        
        self.notify("Jogador conectado! Partida iniciando...")
        self.update_interface()

    def get_local_player(self, players, local_id):
        for player in players:
            if player[1] == local_id:
                return player
        return None
    
    def get_remote_player(self, players, local_id):
        for player in players:
            if player[1] != local_id:
                return player
        return None
    
    def receive_withdrawal_notification(self):
        """Recebe a notificação de que o outro jogador saiu da partida."""
        self.set_match_status(5)
        self.notify("O outro jogador saiu da partida. Voltando para a tela inicial em 5 segundos...")
        self.interface.root.after(5000, self.main_controller.show_menu)
                
    def verify_card_equity(self):
        """Verifica quantas cartas de diferença entre os jogadores."""
        local_cards = self.local_player.card_number
        remote_cards = self.remote_player.card_number
        
        if remote_cards > local_cards:
            return remote_cards - local_cards
        
        return 0
                
    def receive_move(self, move_data):
        
        nature = move_data["nature"]

        match nature:
            case "game_over":
                self.set_match_status(2)
                winner = self.check_winner()
                self.interface.display_winner(winner)
                return
            
            case "normal_play":
                self.deck.update_deck(move_data["deck"])
                self.board.update_board(move_data["board"])
                self.remote_player.update_card_number(move_data["remote_card_number"])
                self.remote_player.update_score(move_data["remote_score"])
                
                cards = self.verify_card_equity()
                              
                for _ in range(cards):
                    self.buy_card("system")
                    
                self.switch_turn()
                self.set_match_status(3)
                    
            case "buy_card":
                self.deck.update_deck(move_data["deck"])
                self.remote_player.update_card_number(move_data["remote_card_number"])
                
                cards = self.verify_card_equity()
                
                for _ in range(cards):
                    self.buy_card("system")

                self.switch_turn()
                    
            case "dealing_initial_cards":
                self.deck.update_deck(move_data["deck"])
                self.local_player.update_hand(move_data["local_hand"])
                self.local_player.update_card_number(len(self.local_player.cards))
                self.remote_player.update_card_number(move_data["remote_card_number"])
                print(f"Cartas recebidas!: {self.deck.deck}")
                self.update_interface()

        
        # self.unblock_all_lines()
        self.update_interface()
        # self.switch_turn()
    
    def send_move(self, move_nature):
        """Envia o movimento para o adversário."""
        move_data = {
            "nature": move_nature,
            "board": self.board.board,
            "deck": self.deck.deck,
            "local_hand": self.remote_player.cards,
            "remote_card_number": self.local_player.card_number,
            "remote_score": self.local_player.score,
            "match_status": "next"
        }
        self.dog_actor.send_move(move_data)
    
    def update_interface(self):
        informations = {
            "j2_fichas": len(self.remote_player.cards),
            "j2_pontos": self.remote_player.score,
            "j1_pontos": self.local_player.score,
            "j1_fichas": self.local_player.cards,
            "shop_size": len(self.deck.deck),
            "board": self.board.board,
            "notifications": self.notification_manager.notifications,
        }
        
        if self.interface.root and self.interface.root.winfo_exists():
            self.interface.root.after(0, lambda: self.interface.update(informations))
            
    def notify(self, message: str):
        """Notifica o jogador."""
        self.notification_manager.add_notification(message)
        self.update_interface()
        
    def get_match_status(self):
        return self.match_status   
    
    def reset_game(self):
        """Reseta o jogo."""
        
        match_status = self.get_match_status()
        
        if match_status == 2 or match_status == 5:
            self.remote_player.reset()
            self.local_player.reset()
            self.board.reset()
            self.deck.reset()
            self.notification_manager.reset()
            self.set_match_status(1)
            self.update_interface()


    def put_card(self, i: int, j: int):
        """Coloca uma carta no tabuleiro."""
    
        selected_card = self.local_player.selected_card
        
        if selected_card != None:
            self.board.put_card(selected_card, i, j)
            self.local_player.remove_card(selected_card)
            
            for i in range(10):
                line = self.board.get_line(i)
                
                if sum(line) == 10:
                    self.board.clear_line(i)
                    self.local_player.add_score(4)
            
            self.local_player.select_card(None)
            
            self.switch_turn()
            self.set_match_status(4)
            
            self.update_interface()
            self.send_move("normal_play")
            
    
        
    def select_card(self, value):
        if not self.local_player.turn:
            self.notify("Aguarde sua vez para selecionar uma carta!")
            return
        
        self.interface.render_board()
        
        self.local_player.select_card(value)
        
        available_moves = self.check_available_moves(value)
        
        for i in range(len(available_moves)):
            if not available_moves[i]:
                self.interface.block_line(i)

    def attribute_winner(self):
        if self.local_player.score > self.remote_player.score:
            self.local_player.won = True
            self.remote_player.won = False
        else:
            self.local_player.won = False       
            self.remote_player.won = True
            
    def check_available_moves(self, value) -> list:
        
        lines = [True for _ in range(10)]
        
        for i in range(10):
            
            line = self.board.get_line(i)
            
            cards_put = 4 - line.count(0)
            
            match cards_put:
                case 1:
                    if sum(line) + value > 8:
                        lines[i] = False
                case 2:
                    if sum(line) + value > 9:
                        lines[i] = False
                case 3:
                    if sum(line) + value != 10:
                        lines[i] = False
        
        return lines
    
    def get_player_turn(self):
        if self.local_player.turn:
            return self.local_player
        else:
            return self.remote_player
    
    def buy_card(self, called: str = "player"):
        """Compra uma carta."""

        if called == "player":
            player = self.get_player_turn()
            
            if player != self.local_player:
                self.notify("Aguarde seu turno para comprar uma carta!")
                return
            
            cards = self.local_player.get_cards()
            
            for card in cards:
                availables = self.check_available_moves(card)
                
                if any(availables):
                    self.notify("Ainda há jogadas disponíveis, não é possível comprar cartas.")
                    return
        
        empty = self.deck.is_empty()
        
        if not empty:
            card = self.deck.buy_card()
            self.local_player.add_card(card)
            
            if called == "player":
                self.switch_turn()
                self.send_move("buy_card")
                
            self.update_interface()
        
        else:
            
            self.notify("Baralho está vazio! Não é possível comprar cartas.")
            
            if called == "system":
                
                cards = self.local_player.get_cards()
                
                for card in cards:
                    availables = self.check_available_moves(card)
                    
                    if any(availables):
                        self.update_interface()
                        return
            
            self.set_match_status(2)
            
            winner = self.check_winner()
            
            self.interface.display_winner(winner)
            
            self.switch_turn()
            
            self.send_move("game_over")
            
            
    def check_winner(self):
        if self.local_player.score >= self.remote_player.score:
            return True
        else:
            return False
            
    def set_match_status(self, status: int):
        self.match_status = status