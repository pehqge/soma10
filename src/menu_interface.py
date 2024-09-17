from interface import Interface
from tkinter import NW
from PIL import ImageTk
import math


class MenuInterface(Interface):
    def __init__(self, root, main_controller):
        super().__init__(root)
        self.main_controller = main_controller
        self.setup()

    def setup(self):
        self.frame.pack(fill='both', expand=True)
        self.canvas.pack()

        # Load images
        self.images['bg'] = ImageTk.PhotoImage(file="assets/menu/fundo.png")
        self.canvas.create_image(0, 0, image=self.images['bg'], anchor=NW)

        # Load logo and animate
        self.images['logo'] = ImageTk.PhotoImage(file="assets/menu/logo.png")
        self.logo_canvas = self.canvas.create_image(
            286, 136, image=self.images['logo'], anchor='nw'
        )
        self.direction = 1
        self.animate_logo()

        # Create buttons
        self.create_button("iniciar", 415, 485, self.start_game)
        self.create_button("tutorial", 642, 485, self.show_tutorial)

    def animate_logo(self):
        # Calculate and update the movement using sine function
        self.logo_offset = 4 * math.sin(math.radians(self.direction))
        self.canvas.coords(self.logo_canvas, 286, 136 + self.logo_offset)

        self.direction += 10
        if self.direction >= 360:
            self.direction = 0

        self.frame.after(10, self.animate_logo)

    def create_button(self, name, x, y, command):
        # Load images
        button_image = ImageTk.PhotoImage(file=f"assets/menu/b_{name}.png")
        button_selected_image = ImageTk.PhotoImage(
            file=f"assets/menu/bs_{name}.png"
        )

        # Save images to prevent garbage collection
        self.images[f"{name}_button"] = button_image
        self.images[f"{name}_button_selected"] = button_selected_image

        # Create the button
        self.canvas.create_image(x - 3, y + 8, image=button_selected_image, anchor='nw')
        button_id = self.canvas.create_image(x + 3, y, image=button_image, anchor='nw')

        # Bind events
        self.canvas.tag_bind(
            button_id, "<Enter>", lambda event: self.move_button(event, button_id, x, y, 0, 2)
        )
        self.canvas.tag_bind(
            button_id, "<Leave>", lambda event: self.move_button(event, button_id, x, y, 2, -2)
        )
        self.canvas.tag_bind(button_id, "<Button-1>", lambda event: command())

    def move_button(self, event, button_id, x, y, dx, dy):
        self.canvas.coords(button_id, x + dx, y + dy)

    def start_game(self):
        self.main_controller.start_game()

    def show_tutorial(self):
        self.main_controller.show_tutorial()