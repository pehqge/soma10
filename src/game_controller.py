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
        
        # Envia para a interface os dados do jogo
        self.update_interface()
        
    def start(self):
        """Inicia a partida."""
        
        # Inicia a interface
        self.interface.show()
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