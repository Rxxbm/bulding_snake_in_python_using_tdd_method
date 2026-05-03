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

    def _get_image_name(self, index, body):
        if index == 0: # Cabeça
            if len(body) == 1: return "head_right"
            curr, next_seg = body[0], body[1]
            diff = (curr[0] - next_seg[0], curr[1] - next_seg[1])
            if diff == (-1, 0): return "head_up"
            if diff == (1, 0): return "head_down"
            if diff == (0, -1): return "head_left"
            if diff == (0, 1): return "head_right"
            if diff[0] > 1: return "head_up"
            if diff[0] < -1: return "head_down"
            if diff[1] > 1: return "head_left"
            if diff[1] < -1: return "head_right"
            return "head_right"

        if index == len(body) - 1: # Cauda
            curr, prev_seg = body[index], body[index - 1]
            diff = (curr[0] - prev_seg[0], curr[1] - prev_seg[1])
            if diff == (-1, 0): return "tail_up"
            if diff == (1, 0): return "tail_down"
            if diff == (0, -1): return "tail_left"
            if diff == (0, 1): return "tail_right"
            if diff[0] > 1: return "tail_up"
            if diff[0] < -1: return "tail_down"
            if diff[1] > 1: return "tail_left"
            if diff[1] < -1: return "tail_right"
            return "tail_right"

        curr, prev_seg, next_seg = body[index], body[index - 1], body[index + 1]
        def norm(d):
            if d > 1: return -1
            if d < -1: return 1
            return d
        p_diff = (norm(prev_seg[0] - curr[0]), norm(prev_seg[1] - curr[1]))
        n_diff = (norm(next_seg[0] - curr[0]), norm(next_seg[1] - curr[1]))

        if p_diff[0] == n_diff[0]: return "body_horizontal"
        if p_diff[1] == n_diff[1]: return "body_vertical"
        
        diffs = {p_diff, n_diff}
        if diffs == {(0,-1), (1,0)}: return "body_bottomleft"
        if diffs == {(0,1), (1,0)}: return "body_bottomright"
        if diffs == {(0,-1), (-1,0)}: return "body_topleft"
        if diffs == {(0,1), (-1,0)}: return "body_topright"
        return "body_horizontal"

# O código antigo do terminal continua aqui para ser refatorado depois
class io_handler:
    def __init__(self, dim, speed):
        pass
