import pytest
from io import StringIO
from unittest.mock import patch
from snake_screen import io_handler, Snake


class TestSnakeCriacao:

    def test_snake_comeca_na_posicao_inicial(self):
        snake = Snake(start=(5, 5))
        assert snake.head() == (5, 5)

    def test_snake_comeca_com_tamanho_1(self):
        snake = Snake(start=(5, 5))
        assert len(snake.body()) == 1

