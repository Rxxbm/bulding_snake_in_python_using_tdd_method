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

class TestSnakeMovimento:
    def test_mover_para_baixo(self):
        snake = Snake(start=(5,5))
        snake.move('s')
        assert snake.head() == (6, 5) # Desloca verticalmente e a linha aumenta

