import pygame
import os

class PygameScreen:
    def __init__(self, bounds=(20, 20), cell_size=40):
        self.bounds = bounds
        self.cell_size = cell_size
        self.width = bounds[0] * cell_size
        self.height = bounds[1] * cell_size
        self.display = pygame.display.set_mode((self.width, self.height))
        self.assets = {}
        self._load_assets()

    def _load_assets(self):
        graphics_path = "snake_graphics/Graphics"
        if not os.path.exists(graphics_path): return
        for file in os.listdir(graphics_path):
            if file.endswith(".png"):
                name = file.replace(".png", "")
                img = pygame.image.load(os.path.join(graphics_path, file)).convert_alpha()
                img = pygame.transform.scale(img, (self.cell_size, self.cell_size))
                self.assets[name] = img

# O código antigo do terminal continua aqui para ser refatorado depois
class io_handler:
    def __init__(self, dim, speed):
        pass
