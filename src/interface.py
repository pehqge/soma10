from abc import ABC, abstractmethod
from tkinter import Frame, Canvas

class Interface(ABC):
    def __init__(self, root):
        self.root = root
        self.frame = Frame(root)
        self.images = {}
        self.canvas = Canvas(self.frame)

    @abstractmethod
    def setup(self):
        pass