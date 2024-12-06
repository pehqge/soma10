from tkinter import Tk, PhotoImage
from menu_interface import MenuInterface
from game_controller import GameController
from tkinter import simpledialog

class MainController:
    def __init__(self):
        # Inicializa a janela principal
        self.root = Tk()
        self.root.geometry("1280x720") # Tamanho da janela
        self.root.resizable(False, False)
        self.root.title("Soma10") # Titulo da janela
        icon = PhotoImage(file="assets/icon.png") # Icone do app
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
        player_name = simpledialog.askstring(title="Soma10", prompt="Qual o seu nome?")
        message = dog_actor.initialize(player_name, self.game)
        
        # Se estiver sem conexao, o jogo é encerrado
        if message == "Você está sem conexão":
            simpledialog.messagebox.showinfo("DogActor", "Você está sem conexão, o jogo será encerrado. Tente novamente.")
            self.exit()
            return
        
        else:
            # Exibe a mensagem do DogActor como popup
            simpledialog.messagebox.showinfo("DogActor", message)
        
        # Inicia o loop principal
        self.root.mainloop()
        
        
    def start_game(self):
        """Inicia o jogo."""
        
        self.game.start_match()
        self.main_menu.hide()
        
    def exit(self):
        """Fecha a aplicação."""
        
        self.root.destroy()


