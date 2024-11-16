from game_interface import GameInterface
from board import Board
from player import Player
from card_deck import CardDeck
from notification_manager import NotificationManager

class GameController:
    def __init__(self, main_controller):
        # Inicializa as classes
        self.board = Board()
        self.local_player = Player("local")
        self.remote_player = Player("remote")
        self.deck = CardDeck()
        self.notification_manager = NotificationManager()
        self.interface = GameInterface(main_controller, self)
        self.match_status = None
        
        # Envia para a interface os dados do jogo
        self.update_interface()
        
    def start(self):
        """Inicia a partida."""
        
        # Inicia a interface
        self.interface.show()
        self.interface.start_match() # conexão com o DOG
        self.interface.setup()
        
        # Compra as cartas iniciais para ambos jogadores
        for i in range(3):
            self.local_player.add_card(self.deck.buy_card())
            self.remote_player.add_card(self.deck.buy_card())
            
        # Atualiza a interface
        self.update_interface()
            
            
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

    def equalize_check(self):
        """Compara qual player tem mais fichas"""  
        if len(self.local_player.cards) > len(self.remote_player.cards):
            qtde = len(self.local_player.cards) - len(self.remote_player.cards)
            for i in range(qtde):
                card = self.deck.buy_card()
                self.local_player.add_card(card)
        if len(self.local_player.cards) < len(self.remote_player.cards):
            qtde = len(self.remote_player.cards) - len(self.local_player.cards)
            for i in range(qtde):
                card = self.deck.buy_card()
                self.remote_player.add_card(card)


    def buy_card(self):
        """Compra uma carta."""
        """
        chamar o tributo turn do player para verificar se é o turno do jogador
        """

        self.get_turn_player()
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
        self.local_player.reset()
        self.remote_player.reset()
        self.deck.reset()
        self.notification_manager.reset()
        self.update_interface()


    def get_match_status(self):
        pass
    """
    pegar status como jogaaa irregular, vencedor, perdedor, empate
    """

    def check_avaible_moves(self):

        """
        verifica as jogadas válidas para a carta selecionada
        """
        pass

    def get_turn_player(self):
        """
        retorna o jogador (objeto) da vez
        """
        pass

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