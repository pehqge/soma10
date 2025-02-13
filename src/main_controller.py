from tkinter import Tk, PhotoImage
from menu_interface import MenuInterface
from game_controller import GameController
from tkinter import simpledialog
from ui_tools import UITools

class MainController:
    def __init__(self):
        # Inicializa a janela principal
        self.root = Tk()
        self.root.geometry("1280x720") # Tamanho da janela
        self.root.resizable(False, False)
        self.root.title("Sum10") # Titulo da janela
        icon = PhotoImage(file=UITools(self.root).resource_path("assets/icon.png")) # Icone do app
        self.root.iconphoto(True, icon)
        
        # Inicializa as interfaces
        self.main_menu = MenuInterface(self)
        self.game = GameController(self)
        
        
    def start(self):
        """Inicia o loop principal da interface gráfica."""
        
        # Mostra o menu principal
        self.main_menu.show()
        
        # Inicializa o DogActor
        dog_actor = self.game.dog_actor
        player_name = simpledialog.askstring(title="Sum10", prompt="What's your name?")
        message = dog_actor.initialize(player_name, self.game)
        
        # Se estiver sem conexao, o jogo é encerrado
        if message == "Você está sem conexão":
            simpledialog.messagebox.showinfo("DogActor", "Error with the server. The game will be closed. Please open the game and try again.")
            self.exit()
            return
        
        else:
            # Exibe a mensagem do DogActor como popup
            simpledialog.messagebox.showinfo("Server", "You are connected to the server")
        
        # Inicia o loop principal
        self.root.mainloop()
        
        
    def start_game(self):
        """Inicia o jogo."""
        
        self.game.start_match()
        self.main_menu.hide()
        
    def exit(self):
        """Fecha a aplicação."""
        
        self.root.destroy()


