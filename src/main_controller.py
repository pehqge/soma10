from tkinter import Tk
from menu_interface import MenuInterface
# from tutorial_interface import TutorialInterface
# from game_controller import GameController


class MainController:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("1280x720")
        self.root.resizable(False, False)
        self.root.title("Soma10")

        # Initialize game controller
        # self.game_controller = GameController(self.root, self)

        # Initialize interfaces
        self.menu_interface = MenuInterface(self.root, self)
        # self.tutorial_interface = TutorialInterface(self.root, self)
        # self.game_interface = self.game_controller.game_interface

        # Show the menu interface initially
        self.show_menu()

    def show_menu(self):
        self.hide_all_frames()
        self.menu_interface.frame.pack(fill='both', expand=True)

    # def show_tutorial(self):
    #     self.hide_all_frames()
    #     self.tutorial_interface.frame.pack(fill='both', expand=True)

    def start_game(self):
        self.hide_all_frames()
        # self.game_interface.frame.pack(fill='both', expand=True)
        self.game_controller.start_game()

    def hide_all_frames(self):
        self.menu_interface.frame.pack_forget()
        # self.tutorial_interface.frame.pack_forget()
        # self.game_interface.frame.pack_forget()

    def run(self):
        self.root.mainloop()