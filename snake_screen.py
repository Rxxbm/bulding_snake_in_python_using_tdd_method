import pygame
import os
import sys
from game_engine import GameEngine

class PygameScreen:
    def __init__(self, bounds=(40, 40), cell_size=20):
        pygame.init()
        self.bounds = bounds
        self.initial_cell_size = cell_size
        self.cell_size = cell_size
        self.width = bounds[0] * cell_size
        self.height = bounds[1] * cell_size
        self.display = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("TDD Snake - Pygame")
        self.is_fullscreen = False
        self.assets = {}
        self._load_assets()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 32)
        self.big_font = pygame.font.SysFont("Arial", 64, bold=True)

    def _load_assets(self):
        graphics_path = "snake_graphics/Graphics"
        if not os.path.exists(graphics_path): return
        for file in os.listdir(graphics_path):
            if file.endswith(".png"):
                name = file.replace(".png", "")
                img = pygame.image.load(os.path.join(graphics_path, file)).convert_alpha()
                # O escalonamento agora acontece no momento do desenho ou quando a tela muda
                self.assets[name] = img

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            info = pygame.display.Info()
            self.display = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
            # Recalcular cell_size para preencher a tela
            self.cell_size = min(info.current_w // self.bounds[0], info.current_h // self.bounds[1])
        else:
            self.cell_size = self.initial_cell_size
            self.display = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

    def draw_game(self, engine):
        self.display.fill((175, 215, 70))
        
        # Centralizar o grid se estiver em tela cheia
        offset_x = (self.display.get_width() - (self.bounds[0] * self.cell_size)) // 2
        offset_y = (self.display.get_height() - (self.bounds[1] * self.cell_size)) // 2

        # Frutas
        apple_img = pygame.transform.scale(self.assets["apple"], (self.cell_size, self.cell_size))
        for r, c in engine.fruits:
            self.display.blit(apple_img, (offset_x + c * self.cell_size, offset_y + r * self.cell_size))
        
        # Cobra
        body = engine.snake.body()
        direction = engine.snake.current_dir
        for i, (r, c) in enumerate(body):
            img_name = self._get_image_name(i, body, direction)
            img = pygame.transform.scale(self.assets[img_name], (self.cell_size, self.cell_size))
            self.display.blit(img, (offset_x + c * self.cell_size, offset_y + r * self.cell_size))
        
        pygame.display.flip()

    def draw_game_over(self, score):
        # Overlay escuro
        overlay = pygame.Surface((self.display.get_width(), self.display.get_height()))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.display.blit(overlay, (0, 0))

        text = self.big_font.render("GAME OVER", True, (255, 255, 255))
        score_text = self.font.render(f"Pontuação Final: {score}", True, (255, 255, 255))
        restart_text = self.font.render("Pressione R para Reiniciar ou ESC para Sair", True, (200, 200, 200))

        self.display.blit(text, (self.display.get_width()//2 - text.get_width()//2, self.display.get_height()//2 - 100))
        self.display.blit(score_text, (self.display.get_width()//2 - score_text.get_width()//2, self.display.get_height()//2))
        self.display.blit(restart_text, (self.display.get_width()//2 - restart_text.get_width()//2, self.display.get_height()//2 + 100))
        
        pygame.display.flip()

    def _get_image_name(self, index, body, direction):
        if index == 0:
            dir_map = {'w': 'head_up', 's': 'head_down', 'a': 'head_left', 'd': 'head_right'}
            return dir_map.get(direction, "head_right")
        if index == len(body) - 1:
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

def main():
    DIM = (30, 30)
    engine = GameEngine(bounds=DIM)
    screen = PygameScreen(bounds=DIM, cell_size=20)
    last_input = 'd'
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:
                        engine = GameEngine(bounds=DIM)
                        game_over = False
                        last_input = 'd'
                    if event.key == pygame.K_ESCAPE:
                        running = False
                else:
                    if event.key == pygame.K_UP: last_input = 'w'
                    if event.key == pygame.K_DOWN: last_input = 's'
                    if event.key == pygame.K_LEFT: last_input = 'a'
                    if event.key == pygame.K_RIGHT: last_input = 'd'
                    if event.key == pygame.K_f:
                        screen.toggle_fullscreen()

        if not game_over:
            engine.update(last_input)
            if engine.snake.is_dead():
                game_over = True
            screen.draw_game(engine)
        else:
            screen.draw_game_over(len(engine.snake.body()) - 1)
            
        screen.clock.tick(10)
    pygame.quit()

if __name__ == '__main__': main()
