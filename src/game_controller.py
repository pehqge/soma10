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
        # Recebe o dog_actor criado no menu principal
        self.dog_actor : DogActor = main_controller.dog_server_interface
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
        
        # Envia para a interface os dados do jogo
        self.update_interface()
        
    def start(self, type="local"):
        """Inicia a partida."""
        # Build GUI
        self.interface.show()
        
        # Request to start match
        if self.match_status == 1 and type == "local": # Se o jogo não foi iniciado
            start_status = self.dog_actor.start_match(2) # Tenta conexão com o servidor
            code = start_status.get_code()
            message = start_status.get_message()
            
            if code == "0" or code == "1": # Se não foi possível conectar
                self.interface.toggle_waiting_screen(True, message)
                self.interface.root.after(5000, self.main_controller.show_menu) # volta pro menu
                return

            players = start_status.get_players()
            local_id = start_status.get_local_id()
            local = players[0] if players[0][1] == local_id else players[1]
            remote = players[0] if players[1][1] == local_id else players[1]
            
            # Initialize players
            self.local_player.update_info(local[0], local[1])
            self.remote_player.update_info(remote[0], remote[1])
                
            # Evaluate who starts
            if players[0][2] == "1":
                self.match_status = 3 # Vez do jogador local
                
                self.deck.initialize_deck() # Inicializa o deck
                
                # Compra as cartas iniciais para ambos jogadores
                for i in range(3):
                    self.local_player.add_card(self.deck.buy_card())
                    self.remote_player.add_card(self.deck.buy_card())
                
                    # Manda deck para o adversário
                self.send_move("dealing_inital_cards")
                
        self.interface.setup()
        # Atualiza a interface
        self.update_interface()
        
    def receive_start(self, start_status):
        self.reset_game()
        
        players = start_status.get_players()
        
        local_id = start_status.get_local_id()
        local = players[0] if players[0][1] == local_id else players[1]
        remote = players[0] if players[1][1] == local_id else players[1]
        
        self.local_player.update_info(local[0], local[1])
        self.remote_player.update_info(remote[0], remote[1])
        
        # if players[0][2] == "2":
        self.match_status = 4
        
        # self.interface.remote_update(self.main_controller.hide_menu)
        # self.interface.remote_update(self.main_controller.hide_tutorial)
        # self.interface.remote_update(self.interface.show)
        # self.interface.remote_update(self.update_interface)
    
    def receive_move(self, move_data):
        """Recebe o movimento do adversário."""
        
        move_nature = move_data["nature"]
        
        if move_nature == "dealing_inital_cards":
            self.deck.receive_deck(move_data["deck"])
        
    
    def send_move(self, move_nature):
        """Envia o movimento para o adversário."""
        
        move_data = {"nature": move_nature, 
                     "board": self.board.board, 
                     "oponent_score": self.local_player.score, 
                     "oponent_cards": self.local_player.cards, 
                     "deck": self.deck.deck,
                     "end": self.game_over,
                     "match_status": "next"}
        
        # Envia o estado do jogo para o adversário
        self.dog_actor.send_move(move_data)
    
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
        
    def buy_card(self):
        """Compra uma carta."""
        
        card = self.deck.buy_card() # Retira uma carta do deck
        
        if card is None: # Se o deck estiver vazio
            self.notify("Baralho vazio.")
            
        else:
            self.local_player.add_card(card) # Adiciona a carta ao jogador
            self.notify(f"A carta {card} foi comprada.") # Notifica a compra
            self.update_interface()
    
    def update_interface(self):
        """Envia para a interface as informações atualizadas do jogo. (Tipo um observer)"""

        informations = {"j2_fichas": len(self.remote_player.cards), "j2_pontos": self.remote_player.score, "j1_pontos": self.local_player.score, "j1_fichas": self.local_player.cards, "shop_size": self.deck.size, "board": self.board.board, "notifications": self.notification_manager.notifications}
            
        self.interface.update(informations)
        
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
        
        self.update_interface()