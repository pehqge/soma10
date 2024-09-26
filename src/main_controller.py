from tkinter import Tk, Frame
from menu_interface import MenuInterface
from game_controller import GameController
import gc

class MainController:
    def __init__(self):
        # Inicializa a janela principal
        self.root = Tk()
        self.root.geometry("1280x720")
        self.root.resizable(False, False)
        self.root.title("Soma10")
        
        # Inicializa as interfaces 
        self.main_menu = MenuInterface(self)
        # self.tutorial_menu = TutorialInterface(self.tutorial_frame, self)
        self.game = GameController(self)

    def show_menu(self):
        """Exibe o menu principal."""
        self.reset_application()
        self.main_menu.show()

    def show_tutorial(self):
        """Exibe o tutorial."""
        pass
        
    def start_game(self):
        """Inicia o jogo."""
        self.game.interface.show()
        self.game.reset_game()
        self.game.start()

    def reset_application(self):
        """Remove o jogo antigo e exibe o menu principal."""
        
        for widget in self.root.winfo_children():
            widget.destroy()
        gc.collect()
        self.main_menu = MenuInterface(self)
        self.game = GameController(self)
        
    def start(self):
        """Inicia o loop principal da interface gráfica."""
        self.root.mainloop()
