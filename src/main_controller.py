from tkinter import Tk, PhotoImage
from menu_interface import MenuInterface
from game_controller import GameController
from tutorial_interface import TutorialInterface

class MainController:
    def __init__(self):
        # Inicializa a janela principal
        self.root = Tk()
        self.root.geometry("1280x720") # Tamanho da janela
        self.root.resizable(False, False)
        self.root.title("Soma10") # Titulo da janela
        icon = PhotoImage(file="assets/icon.png") # Icone da janela
        self.root.iconphoto(True, icon)
        
        # Inicializa as interfaces
        self.main_menu = MenuInterface(self)
        self.tutorial_menu = TutorialInterface(self)
        self.game = GameController(self)
        
        
    def setup(self):
        """ Inicializa as interfaces do jogo."""
        
        self.main_menu = MenuInterface(self)
        self.tutorial_menu = TutorialInterface(self)
        self.game = GameController(self)

    def show_menu(self):
        """Exibe o menu principal."""
        
        self.reset_application() # Reseta a aplicação por completo
        self.main_menu.show()

    def show_tutorial(self):
        """Exibe o tutorial."""
        
        self.main_menu.hide()
        self.tutorial_menu.show()
        
    def start_game(self):
        """Inicia o jogo."""
        
        self.main_menu.hide()
        self.tutorial_menu.hide()
        self.game.start_match()

    def reset_application(self):
        """Remove o jogo antigo e exibe o menu principal."""
        
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.setup()
        
    def start(self):
        """Inicia o loop principal da interface gráfica."""
        
        self.root.mainloop()
