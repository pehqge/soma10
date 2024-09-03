from tkinter import Tk, Frame
from menu import MainMenu
from jogo import BoardGame

# Inicialize a janela principal
root = Tk()
root.geometry("1280x720")
root.title("Soma10")

# Cria frames para o MainMenu e BoardGame
main_menu_frame = Frame(root)
game_frame = Frame(root)

# Inicialize o MainMenu e BoardGame
main_menu = MainMenu(main_menu_frame, game_frame)
board_game = BoardGame(game_frame)

root.mainloop()