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
        # Este teste deve falhar pois PygameScreen não existe ou não carrega assets
        assert "apple" in screen.assets
        assert "head_up" in screen.assets
        pygame.quit()
