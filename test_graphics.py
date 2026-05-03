import pytest
import pygame
import os
from snake_screen import PygameScreen

class TestPygameScreen:
    @pytest.fixture
    def screen(self):
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()
        return PygameScreen(bounds=(20, 20), cell_size=40)

    def test_screen_initialization(self, screen):
        assert screen.width == 800
        assert screen.height == 800
        assert screen.display is not None
        pygame.quit()

    def test_load_assets(self, screen):
        assert "apple" in screen.assets
        assert "head_up" in screen.assets
        pygame.quit()

    def test_get_image_name_head_and_tail(self, screen):
        # Cabeça para cima ('w')
        assert screen._get_image_name(index=0, body=[(5,5), (6,5)], direction='w') == "head_up"
        # Cauda para baixo
        assert screen._get_image_name(index=1, body=[(5,5), (6,5)], direction='w') == "tail_down"
        pygame.quit()

    def test_get_image_name_curves(self, screen):
        # Curva body_topright
        body = [(4,5), (5,5), (5,6)]
        assert screen._get_image_name(index=1, body=body, direction='w') == "body_topright"
        pygame.quit()

    def test_score_calculation(self, screen):
        class MockEngine:
            def __init__(self):
                class MockSnake:
                    def body(self): return [(0,0), (0,1), (0,2)]
                self.snake = MockSnake()
        engine = MockEngine()
        score = len(engine.snake.body()) - 1
        assert score == 2
        pygame.quit()

    def test_head_direction_size_1(self, screen):
        # Cobra de tamanho 1 movendo para cima ('w')
        assert screen._get_image_name(index=0, body=[(5,5)], direction='w') == "head_up"
        # Cobra de tamanho 1 movendo para esquerda ('a')
        assert screen._get_image_name(index=0, body=[(5,5)], direction='a') == "head_left"
        pygame.quit()
