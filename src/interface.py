# interface.py
from tkinter import Frame, Canvas
from abc import ABC, abstractmethod
from ui_tools import UITools

class Interface(ABC):
    def __init__(self, main_controller):
        
        # Inicializa o MainController e a janela principal
        self.root = main_controller.root
        self.main_controller = main_controller
        
        # Cria um frame para a interface
        self.frame = Frame(self.root)
        self.canvas = Canvas(self.frame, width=1280, height=720)
        
        # Inicializa a ferramenta de UI
        self.ui_tools = UITools(self.canvas)

    @abstractmethod
    def setup(self):
        """Configura a interface."""
        pass

    def show(self):
        """Exibe a interface."""
        
        self.frame.pack(fill='both', expand=True)
        self.canvas.pack()
        self.setup()

    def hide(self):
        """Esconde a interface."""
        
        self.frame.pack_forget()