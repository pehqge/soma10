from PIL import Image, ImageTk

class Card:
    def __init__(self, value: int):
        self.__value = value
        # self.__image = self.get_card_image()
    
    def get_card_image(self):
        """Retorna uma imagem ImageTk com base no valor da carta."""
        image_path = f"assets/jogo/{self.__value}.png"
        
        try:
            # Carrega a imagem usando PIL
            # image = Image.open(image_path)
            
            # Converte a imagem para um formato compatível com Tkinter
            self.image_tk = ImageTk.PhotoImage(file=image_path)
            
            # return image_tk
        
        except FileNotFoundError:
            print(f"Erro: Imagem da carta com valor {self.__value} não encontrada no caminho '{image_path}'.")
            return None
    
    @property
    def image(self):
        return self.__image
    
    @property
    def value(self):
        return self.__value
    
