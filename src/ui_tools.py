from tkinter import NW, Canvas
from PIL import Image, ImageDraw, ImageFont, ImageTk
import math

class UITools:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        self.images = {}      # Dicionário para armazenar as imagens carregadas
        self.animations = {}  # Dicionário para controlar as animações

    def safe_execute(self, func, *args, **kwargs):
        """Executa métodos de forma segura, verificando a existência do canvas."""
        
        if hasattr(self, 'canvas') and self.canvas.winfo_exists():
            return func(*args, **kwargs)
        return None

    def load_image(self, key: str, filepath: str):
        """Armazena uma imagem no dicionário de imagens."""
        
        if key in self.images:
            return self.images[key]
        
        image = ImageTk.PhotoImage(file=filepath)
        self.images[key] = image
        return image

    def display_image(self, key: str, x: int, y: int, anchor=NW):
        """Exibe uma imagem no canvas usando a chave fornecida."""
        
        image = self.images.get(key)
        if image:
            # Use safe_execute to ensure thread safety
            image_id = self.safe_execute(self.canvas.create_image, x, y, image=image, anchor=anchor)
            return image_id
        else:
            raise ValueError(f"Imagem com a chave '{key}' não encontrada.")
        
    def load_and_display(self, key: str, filepath: str, x: int, y: int, anchor=NW):
        """Carrega e exibe uma imagem no canvas."""
    
        image = self.load_image(key, filepath)
        return (image, self.display_image(key, x, y, anchor))

    def animate_image(self, image_id, x: int, y: int, amplitude=4, speed=10):
        """Anima uma imagem em movimento vertical usando a função seno."""
        
        # Armazena o estado da animação dentro do dicionário animations
        # Cada image_id terá seu próprio estado de 'direction'
        if image_id not in self.animations:
            self.animations[image_id] = {'direction': 0}

        def animate():
            """Função interna que atualiza a posição da imagem repetidamente."""
            
            # Recupera o estado atual da animação
            state = self.animations[image_id]
            direction = state['direction']

            # Calcula a nova posição da imagem
            offset = amplitude * math.sin(math.radians(direction))
            new_y = y + offset

            # Atualiza a posição da imagem no canvas de forma thread-safe
            self.safe_execute(self.canvas.coords, image_id, x, new_y)

            # Atualiza o estado da direção
            direction += speed
            if direction >= 360:
                direction = 0
            state['direction'] = direction

            # Agenda a próxima chamada da animação
            self.canvas.after(10, animate)

        # Inicia a animação
        animate()

    def create_button(self, name: str, x: int, y: int, command: callable):
        """Cria um botão que controla hover e eventos de clique."""
        
        # Carrega as imagens do botão
        self.load_image(f'{name}_button', f"assets/menu/b_{name}.png")  # imagem do botao
        self.load_image(f'{name}_button_selected', f"assets/menu/bs_{name}.png")  # imagem da sombra do botao

        # Exibe os botões no canvas
        self.display_image(f'{name}_button_selected', x - 3, y + 8)
        button_id = self.display_image(f'{name}_button', x + 3, y)

        # Vincula os eventos ao botão de forma thread-safe
        def on_enter(event):
            self.safe_execute(self.canvas.coords, button_id, x, y + 2)

        def on_leave(event):
            self.safe_execute(self.canvas.coords, button_id, x + 3, y)

        def on_click(event):
            command()

        # Realiza os tratamentos de evento do botão
        self.canvas.tag_bind(button_id, "<Enter>", on_enter)  # Mouse sobre o botão
        self.canvas.tag_bind(button_id, "<Leave>", on_leave)  # Mouse quando sai do botão
        self.canvas.tag_bind(button_id, "<Button-1>", on_click)  # Clique esquerdo no botão

        # Retorna o ID do botão para controle adicional, se necessário
        return button_id
    
    def create_text_image(self, text: str, size: int, color: str, font: str, width: int, height: int, x_offset=0, y_offset=0, center=False):
        """Cria uma imagem Pillow do texto"""
        
        font_path = f"assets/jogo/{font}.ttf"
        font_obj = ImageFont.truetype(font_path, size)

        # Cria uma imagem com fundo transparente
        image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)

        if center:
            # Calcula o tamanho do texto
            text_bbox = font_obj.getbbox(text)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            # Ajusta o deslocamento para centralizar o texto
            x_offset = (width - text_width) // 2
            y_offset = (height - text_height) // 2

        draw.text((x_offset, y_offset), text, font=font_obj, fill=color)
        
        return image

    def write_text(self, text: str, x: int, y: int, size: int, color: str, font: str, width=400, height=100, x_offset=0, y_offset=0, center=False):
        """Coloca na tela um texto com a fonte fornecida."""
        
        # Cria a imagem do texto com a centralização se necessário
        image = self.create_text_image(text, size, color, font, width, height, x_offset, y_offset, center)

        # Converte a imagem PIL para ImageTk
        text_image = ImageTk.PhotoImage(image)

        # Armazena a imagem para evitar garbage collection
        self.images[x * y] = text_image

        # Se `center=True`, ajusta `x` e `y` para centralizar o texto
        if center:
            x -= width // 2
            y -= height // 2
            anchor = 'center'
        else:
            anchor = NW

        # Exibe a imagem no canvas de forma thread-safe
        image_id = self.safe_execute(self.canvas.create_image, x, y, image=text_image, anchor=anchor)

        return image_id
    
    def create_card(self, card_number: int, quantity: int, on_click=None):
        """Cria uma ficha com base no número da ficha e quantidade fornecida."""
        
        card_pos = [(145, 235), (145, 346), (145, 458), (145, 569), (251, 290), (251, 402), (251, 513)]  # Posições das fichas
        x, y = card_pos[card_number - 1]
        
        # Determina a chave da imagem com base nos parâmetros
        image_key = f"card_{card_number}_{quantity}"

        # Verifica se a imagem já foi carregada
        if image_key not in self.images:
            # Seleciona o arquivo de imagem adequado
            if quantity == 0:
                image_filename = f"assets/jogo/{card_number}o.png"
                interactive = False
            elif quantity == 1:
                image_filename = f"assets/jogo/{card_number}.png"
                interactive = True
            else:
                image_filename = f"assets/jogo/{card_number}p.png"
                interactive = True

            # Carrega a imagem base
            try:
                base_image = Image.open(image_filename).convert("RGBA")
            except FileNotFoundError:
                raise FileNotFoundError(f"Imagem não encontrada: {image_filename}")

            # Se quantity > 1, renderiza o texto e sobrepõe na imagem
            if quantity > 1:
                # Cria a imagem do texto
                text_image = self.create_text_image(
                    text=str(quantity), size=29, color='#FF648D',
                    font='quicksand bold', width=base_image.width,
                    height=base_image.height, x_offset=90, y_offset=14
                )
                # Sobrepõe o texto na imagem base
                base_image = Image.alpha_composite(base_image, text_image)

            # Cria a imagem redimensionada para animação (apenas se interativa)
            if interactive:
                resized_image = base_image.resize(
                    (int(base_image.width * 1.12), int(base_image.height * 1.12))
                )
                resized_image_tk = ImageTk.PhotoImage(resized_image)
                self.images[f"{image_key}_resized"] = resized_image_tk

            # Converte a imagem base para PhotoImage
            base_image_tk = ImageTk.PhotoImage(base_image)

            # Armazena a imagem no dicionário
            self.images[image_key] = base_image_tk
        else:
            # Recupera as imagens já carregadas
            base_image_tk = self.images[image_key]
            resized_image_tk = self.images.get(f"{image_key}_resized")
            interactive = quantity != 0

        # Cria a imagem no canvas de forma thread-safe
        image_id = self.safe_execute(self.canvas.create_image, x, y, image=base_image_tk, anchor='center')

        # Vincula eventos de animação e clique, se aplicável
        if interactive:
            # Animação ao passar o mouse
            if resized_image_tk:
                def on_enter(event):
                    self.safe_execute(self.canvas.itemconfig, image_id, image=resized_image_tk)
                def on_leave(event):
                    self.safe_execute(self.canvas.itemconfig, image_id, image=base_image_tk)
                self.canvas.tag_bind(image_id, "<Enter>", on_enter)
                self.canvas.tag_bind(image_id, "<Leave>", on_leave)

            # Evento de clique
            if on_click:
                self.canvas.tag_bind(image_id, "<Button-1>", on_click)

        return image_id
    
    def dark_cell(self, card_number: int, i: int, j: int):
        """
        Escurece uma célula do tabuleiro com base no valor da posição no tabuleiro.
        
        Parâmetros:
            i (int): Linha da célula.
            j (int): Coluna da célula.
            card_number (int): Valor da posição no tabuleiro (usado para identificar a imagem).
        """
        
        if card_number != 0:
            return

        # Verifica se a versão escurecida já foi carregada
        dark_image_key = f"dark_{card_number}"
        if dark_image_key not in self.images:
            # Carrega a imagem original
            original_image = Image.open(f"assets/jogo/{card_number}.png").convert("RGBA")
            # Reduz o brilho da imagem
            dark_image = original_image.point(lambda p: p * 0.5)
            # Converte a imagem para o formato compatível com Tkinter
            dark_image_tk = ImageTk.PhotoImage(dark_image)
            # Armazena a imagem escurecida em cache
            self.images[dark_image_key] = dark_image_tk
        else:
            # Usa a imagem escurecida em cache
            dark_image_tk = self.images[dark_image_key]
            
        x = 454 + 124 * i
        y = 235 + 124 * j

        self.safe_execute(self.canvas.create_image, x, y, image=dark_image_tk, anchor="center")

    def create_board_cell(self, card_number: int, i: int, j: int, on_click=None):
        """Cria uma célula do tabuleiro com base no número da carta e índices fornecidos."""
        
        # Coordenadas da célula, baseada na posicao no tabuleiro
        x = 454 + 124 * i
        y = 235 + 124 * j

        # Carrega a imagem da célula vazia
        empty_cell_key = 'cell_empty'
        
        if empty_cell_key not in self.images:
            empty_cell_image = Image.open("assets/jogo/0.png").convert("RGBA")
            empty_cell_tk = ImageTk.PhotoImage(empty_cell_image)
            self.images[empty_cell_key] = empty_cell_tk
        else:
            empty_cell_tk = self.images[empty_cell_key]

        # Cria a célula vazia no canvas de forma thread-safe
        cell_id = self.safe_execute(self.canvas.create_image, x, y, image=empty_cell_tk, anchor='center')

        # Se a célula estiver vazia, vincula o evento de clique
        if card_number == 0:
            if on_click:
                self.canvas.tag_bind(cell_id, "<Button-1>", on_click)
        else:
            # Coloca a imagem da carta na célula
            card_key = f'card_{card_number}'
            if card_key not in self.images:
                card_image = Image.open(f"assets/jogo/{card_number}.png").convert("RGBA").resize((110, 110))
                card_tk = ImageTk.PhotoImage(card_image)
                self.images[card_key] = card_tk
            else:
                card_tk = self.images[card_key]

            # Coloca a carta na célula em cima da célula vazia
            self.safe_execute(self.canvas.create_image, x, y, image=card_tk, anchor='center')

        return cell_id

    def merge_text_to_image(self, key: str, text: str, image_path: str, font_name: str, font_size: int, color: str, x_offset=0, y_offset=0):
        """Adiciona um texto a uma imagem e armazena no dicionário de imagens."""
        
        # Essa função pode receber um número inteiro ou uma string, se inteiro, converte para string
        if isinstance(text, int):
            text = str(text)
        
        # Abre a imagem base
        base_image = Image.open(image_path).convert("RGBA")
    
        # Cria um objeto de desenho
        draw = ImageDraw.Draw(base_image)

        # Carrega a fonte
        font_path = f"assets/jogo/{font_name}.ttf"
        font = ImageFont.truetype(font_path, font_size)

        if len(text) > 1:  # Se o texto tiver mais de um caractere, centraliza
            text_position = (x_offset, y_offset)
        else:
            text_position = (x_offset+6, y_offset)
            
        # Escreve o texto na imagem
        draw.text(text_position, text, font=font, fill=color)

        # Converte a imagem para PhotoImage
        result_image = ImageTk.PhotoImage(base_image)
        
        # Adiciona a imagem ao dicionário de imagens
        self.images[key] = result_image

        return base_image
    
    def create_shop_button(self, quantity: int, command: callable):
        """Cria um botão para a loja de itens."""
        
        numero_x = 145 + (len(str(quantity))-1) * 2
        
        base_image = self.merge_text_to_image("shop", quantity, "assets/jogo/comprar.png", "font_kid", 30, "#FF648D", numero_x, 21)
        
        self.create_resizable_button(base_image, 640, 87, command, anchor="center")
        
    def create_resizable_button(self, image: str | Image.Image, x: int, y: int, command: callable, anchor="center", scale=1.08):
        """Cria um botão com redimensionamento no efeito de hover."""
        
        # Se a imagem for do tipo string, carrega a imagem do caminho
        if isinstance(image, str):
            try:
                base_image = Image.open(image).convert("RGBA")
            except FileNotFoundError:
                raise FileNotFoundError(f"Imagem não encontrada: {image}")
        elif isinstance(image, Image.Image):
            base_image = image
        else:
            raise ValueError("O parâmetro 'image' deve ser uma string (caminho da imagem) ou uma instância de PIL.Image.")
        
        # Converte a imagem base para PhotoImage
        base_image_tk = ImageTk.PhotoImage(base_image)
        
        # Adiciona a imagem original ao dicionário
        image_key = f"button_{x}_{y}"
        self.images[image_key] = base_image_tk

        # Redimensiona a imagem para o efeito de hover
        width, height = base_image.size
        resized_image = base_image.resize((int(width * scale), int(height * scale)))

        # Converte a imagem redimensionada para PhotoImage
        resized_image_tk = ImageTk.PhotoImage(resized_image)

        # Armazena a imagem redimensionada no dicionário
        self.images[f"{image_key}_resized"] = resized_image_tk

        # Exibe a imagem no canvas e obtém o ID da imagem de forma thread-safe
        image_id = self.safe_execute(self.canvas.create_image, x, y, image=base_image_tk, anchor=anchor)

        def on_enter(event):
            self.safe_execute(self.canvas.itemconfig, image_id, image=self.images[f"{image_key}_resized"], anchor=anchor)

        def on_leave(event):
            self.safe_execute(self.canvas.itemconfig, image_id, image=self.images[image_key], anchor=anchor)

        def on_click(event):
            command()

        # Vincula os eventos ao botão para o efeito de hover
        self.canvas.tag_bind(image_id, "<Enter>", on_enter)
        self.canvas.tag_bind(image_id, "<Leave>", on_leave)
        self.canvas.tag_bind(image_id, "<Button-1>", on_click)
        
        return image_id
        
    def clear_canvas(self):
        """Remove todos os elementos do canvas, se ele existir."""
        
        if self.canvas.winfo_exists():
            self.safe_execute(self.canvas.delete, "all")