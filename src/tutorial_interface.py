from ui_tools import UITools
from interface import Interface

class TutorialInterface(Interface):
    def __init__(self, main_controller):
        super().__init__(main_controller)
        self.setup()
        
    def setup(self):
        # Carrega fundo e imagem do tutorial
        self.ui_tools.load_and_display("bg", "assets/jogo/fundo.png", 0, 0)
        self.ui_tools.load_and_display("tutorial", "assets/menu/tutorial.png", 0, 0)
        
        # Carrega botão que volta ao menu principal
        self.ui_tools.create_resizable_button("assets/jogo/close.png", 1175, 196, self.main_controller.show_menu)