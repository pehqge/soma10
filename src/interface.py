# interface.py
from tkinter import Frame, Canvas
from abc import ABC, abstractmethod
from ui_tools import UITools

class Interface(ABC):
    def __init__(self, main_controller):
        # Inicializa o MainController e a janela principal
        self.main_controller = main_controller
        self.root = main_controller.root
        
        # Cria um frame para a interface
        self.frame = Frame(self.root)
        self.show()
        
        # Inicializa a ferramenta de UI
        self.ui_tools = UITools(self.canvas)


    @abstractmethod
    def setup(self):
        pass

    def show(self):
        self.frame.pack(fill='both', expand=True)
        self.canvas = Canvas(self.frame, width=1280, height=720)
        self.canvas.pack()

    def hide(self):
        self.frame.pack_forget()