from tkinter import Tk, Canvas, NW
from PIL import ImageTk  
import math  

class MainMenu:
    def __init__(self):
        # Inicia a tela
        self.mainWindow = Tk()
        self.mainWindow.title("Soma10")
        self.mainWindow.geometry("1280x720")
        self.mainWindow.resizable(False, False)
        self.canvas = Canvas(self.mainWindow, width=1280, height=720)
        self.canvas.pack()

        # Inicia Background
        self.bg_image = ImageTk.PhotoImage(file="assets/menu/fundo.png")
        self.canvas.create_image(0, 0, image=self.bg_image, anchor=NW)
        
        # Inicia Logo e anima
        self.logo_image = ImageTk.PhotoImage(file="assets/menu/logo.png")
        self.logo_canvas = self.canvas.create_image(286, 136, image=self.logo_image, anchor=NW)
        self.direction = 1 
        self.animate_logo()
        
        # Inicia os botões
        self.create_button("iniciar", 415, 485)
        self.create_button("tutorial", 642, 485)

        # Inicia o programa
        self.mainWindow.mainloop()

    # Funcao para gerenciar a animacao da logo do menu
    def animate_logo(self):
        # Calculo e atualizacao do movimento pela funcao seno
        self.logo_offset = 4 * math.sin(math.radians(self.direction)) 
        self.canvas.coords(self.logo_canvas, 286, 136 + self.logo_offset)
        
        self.direction += 10 
        if self.direction >= 360:
            self.direction = 0

        self.mainWindow.after(10, self.animate_logo)
        
    # Funcao para criar e gerar um botao na tela
    def create_button(self, name, x, y):
        # Carrega as imagens
        button_image = ImageTk.PhotoImage(file=f"assets/menu/b_{name}.png")
        button_selected_image = ImageTk.PhotoImage(file=f"assets/menu/bs_{name}.png")

        # Salva como atributo para ele ser gerado
        setattr(self, f"{name}_image", button_image)
        setattr(self, f"{name}_selected_image", button_selected_image)

        # Coloca o botao na tela
        self.canvas.create_image(x - 3, y + 8, image=button_selected_image, anchor=NW)
        button_id = self.canvas.create_image(x + 3, y, image=button_image, anchor=NW)
        
        # Vincula os eventos de entrada e saída de mouse
        self.canvas.tag_bind(button_id, "<Enter>", lambda event: self.move_button(event, button_id, x, y, 0, 2))
        self.canvas.tag_bind(button_id, "<Button-1>", lambda event: self.move_button(event, button_id, x, y, -2, 8))
        self.canvas.tag_bind(button_id, "<Leave>", lambda event: self.move_button(event, button_id, x, y, 2, -2))

    # Funcao para gerenciar o movimento do botao quando passar o mouse por cima
    def move_button(self, event, button_id, x, y, dx, dy):
        self.canvas.coords(button_id, x + dx, y + dy)


MainMenu()