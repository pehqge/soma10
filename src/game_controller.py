from game_interface import GameInterface
from board import Board
from player import Player
from card_deck import CardDeck
from notification_manager import NotificationManager

class GameController:
    def __init__(self, main_controller):
        self.board = Board()
        self.local_player = Player("local")
        self.remote_player = Player("remote")
        self.deck = CardDeck()
        self.notification_manager = NotificationManager()
        self.interface = GameInterface(main_controller, self)
        
        self.update_interface()
        
    def start(self):
        # Inicia a interface
        self.interface.setup()
        
        # Compra as cartas iniciais
        for i in range(3):
            self.local_player.add_card(self.deck.buy_card())
            self.remote_player.add_card(self.deck.buy_card())
            
        # Atualiza a interface
        self.update_interface()
            
    
    def reset_game(self):
        self.board.reset_board()
        self.deck.reset_deck()
        self.local_player.reset()
        self.remote_player.reset()
    
    def put_card(self, i, j):
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
        
        card = self.deck.buy_card()
        if card is None:
            self.notify("Baralho vazio.")
        else:
            self.local_player.add_card(card)
            self.notify(f"A carta {card} foi comprada.")
            self.update_interface()
    
    def update_interface(self):
        informations = {"j2_fichas": len(self.remote_player.cards), "j2_pontos": self.remote_player.score, "j1_pontos": self.local_player.score, "j1_fichas": self.local_player.cards, "shop_size": self.deck.size, "board": self.board.board, "notifications": self.notification_manager.notifications}
        self.interface.update(informations)
        
    def notify(self, message):
        self.notification_manager.add_notification(message)
        self.update_interface()