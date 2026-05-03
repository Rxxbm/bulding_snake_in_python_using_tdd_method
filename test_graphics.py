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
        # Cabeça para cima
        assert screen._get_image_name(index=0, body=[(5,5), (6,5)]) == "head_up"
        # Cauda para baixo
        assert screen._get_image_name(index=1, body=[(5,5), (6,5)]) == "tail_down"
        pygame.quit()

    def test_get_image_name_curves(self, screen):
        # Curva body_topright
        body = [(4,5), (5,5), (5,6)]
        assert screen._get_image_name(index=1, body=body) == "body_topright"
        pygame.quit()
