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
        self.game_over = False
        self.dog_actor = DogActor()
        self.connection = False
        
        self.update_interface()
        
    def start(self):
        """Inicia a partida ao clicar em 'Iniciar Jogo'."""
        self.interface.show()
        self.interface.setup()

        # Inicializa o DogActor
        player_name = simpledialog.askstring(title="Player identification", prompt="Qual o seu nome?")
        message = self.dog_actor.initialize(player_name, self)
        self.notify(message)
        
        self.notify("Conectando ao servidor...")
        self.request_start()

    def request_start(self):
        """Solicita ao servidor o início da partida."""
        # Se o jogo já está conectado, não continue tentando
        if self.connection:
            return

        if self.match_status == 1:
            start_status = self.dog_actor.start_match(2)
            code = start_status.get_code()
            
            if code in ["0", "1"]:
                # Exibe notificação informando que está tentando conectar
                self.notify("Aguardando outro jogador...")
                # Tenta novamente em 2 segundos se ainda não estiver conectado
                self.interface.root.after(2000, self.request_start)
            else:
                self.connection = True
                self.notify("Jogador encontrado! Partida iniciando...")
                self.start_game(start_status)

    def start_game(self, start_status):
        """Configura o jogo após ambos os jogadores estarem conectados."""
        print("Partida iniciada!")
        
        self.reset_game()
        players = start_status.get_players()
        local_id = start_status.get_local_id()

        # Determina qual jogador começa
        if players[0][1] == local_id:
            self.match_status = 3  # Vez do jogador local (inicia baralho)
            self.deck.initialize_deck()
            
            for _ in range(3):
                self.local_player.add_card(self.deck.buy_card())
                self.remote_player.add_card(self.deck.buy_card())
            
            self.send_move("dealing_initial_cards")
        else:
            self.match_status = 4  # Vez do jogador remoto
        
        self.notify("Partida iniciada!")
        self.update_interface()
    
    def receive_start(self, start_status):
        """Recebe a notificação do início da partida para o jogador que estava esperando."""
        print("Partida recebida!")

        self.connection = True

        self.reset_game()
        self.match_status = 4  # Vez do jogador remoto

        players = start_status.get_players()
        local_id = start_status.get_local_id()
        local = players[0] if players[0][1] == local_id else players[1]
        remote = players[0] if players[1][1] != local_id else players[1]

        self.local_player.update_info(local[0], local[1])
        self.remote_player.update_info(remote[0], remote[1])

        # Atualiza a interface para o jogador que estava esperando
        self.update_interface()
        
        self.notify("Jogador conectado! Partida iniciando...")

    def receive_move(self, move_data):
        """Recebe o movimento do adversário."""
        move_nature = move_data["nature"]
        
        if move_nature == "dealing_initial_cards":
            self.deck.receive_deck(move_data["deck"])
            self.update_interface()
            
        elif move_nature == "normal_play":
            print("recebido")
            self.board.board = move_data["board"]
            self.local_player.score = move_data["local_score"]
            self.local_player.cards = move_data["local_hand"]
            self.deck.deck = move_data["deck"]
            self.game_over = move_data["end"]
            self.match_status = 3
            self.update_interface()
        
        elif move_nature == "buy_card":
            self.deck.deck = move_data["deck"]
            
        # Verificar se a interface ainda está disponível antes de atualizar
        if self.interface.root and self.interface.root.winfo_exists():
            self.update_interface()
    
    def send_move(self, move_nature):
        """Envia o movimento para o adversário."""
        move_data = {
            "nature": move_nature,
            "board": self.board.board,
            "local_score": self.local_player.score,
            "local_hand": self.local_player.cards,
            "deck": self.deck.deck,
            "end": self.game_over,
            "match_status": "next"
        }
        self.dog_actor.send_move(move_data)
    
    def update_interface(self):
        informations = {
            "j2_fichas": len(self.remote_player.cards),
            "j2_pontos": self.remote_player.score,
            "j1_pontos": self.local_player.score,
            "j1_fichas": self.local_player.cards,
            "shop_size": self.deck.size,
            "board": self.board.board,
            "notifications": self.notification_manager.notifications
        }
        self.interface.root.after(0, lambda: self.interface.update(informations))
        print('self.update_interface: interface atualizada')
            
    def notify(self, message: str):
        """Notifica o jogador."""
        self.notification_manager.add_notification(message)
        self.update_interface()
        
    def reset_game(self):
        """Reseta o jogo."""
        self.board.reset()
        self.deck.reset()
        self.local_player.reset()
        self.remote_player.reset()
        self.notification_manager.reset()
        self.match_status = 1
        self.game_over = False
        
        
    def put_card(self, i: int, j: int):
        """Coloca uma carta no tabuleiro."""
    
        # Confere se o jogador possui uma carta selecionada
        if self.local_player.selected_card is None:
            return
        
        card = self.local_player.selected_card # Pega a carta selecionada
        self.board.put_card(card, i, j) # Coloca a carta no tabuleiro
        self.local_player.remove_card(card) # Remove a carta do jogador
        
        self.buy_card() # Compra uma nova carta
        
        self.update_interface() # Atualiza a interface
        
        self.send_move("put_card")
        
    def buy_card(self):
        """Compra uma carta."""
        
        card = self.deck.buy_card() # Retira uma carta do deck
        
        if card is None: # Se o deck estiver vazio
            self.notify("Baralho vazio.")
            
        else:
            self.local_player.add_card(card) # Adiciona a carta ao jogador
            self.notify(f"A carta {card} foi comprada.") # Notifica a compra
            self.update_interface()
        