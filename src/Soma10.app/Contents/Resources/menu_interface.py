from interface import Interface

class MenuInterface(Interface):
    def __init__(self, main_controller):
        super().__init__(main_controller)
        
    def setup(self):
        
        # Carrega e exibe o background
        self.ui_tools.load_and_display("bg", "assets/menu/fundo.png", 0, 0)
        
        # Carrega e exibe a logo
        self.ui_tools.load_image("logo", "assets/menu/logo.png")
        logo_id = self.ui_tools.display_image("logo", 286, 136)
        
        # Anima a logo
        self.ui_tools.animate_image(logo_id, 286, 136, speed=4)
        
        # Cria os botões
        self.ui_tools.create_button("iniciar", 460, 485, self.main_controller.start_game)