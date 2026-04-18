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
    def test_mover_para_direita(self):
        snake = Snake(start=(5,5))
        snake.move('d')
        assert snake.head() == (5, 6) # Desloca verticalmente e a linha aumenta
    def test_mover_para_esquerda(self):
        snake = Snake(start=(5,5))
        snake.move('a')
        assert snake.head() == (5, 4) # Desloca verticalmente e a linha aumenta
    def test_mover_para_cima(self):
        snake = Snake(start=(5,5))
        snake.move('w')
        assert snake.head() == (4, 5) # Desloca verticalmente e a linha aumenta
    def test_corpo_segue_cabeca(self):
        snake = Snake(start=(5,5))
        snake.grow()
        snake.move('d')
        assert snake.body() == [(5, 6), (5, 5)]

class TestSnakeColisao:
    def test_nao_pode_inverter_direcao(self):
        snake = Snake(start=(5, 5))
        snake.move('d')
        snake.move('a')
        assert snake.head() == (5, 7)
        snake = Snake(start=(5, 5))
        snake.move('a')
        snake.move('d')
        assert snake.head() == (5, 3)
        snake = Snake(start=(5, 5))
        snake.move('w')
        snake.move('s')
        assert snake.head() == (3, 5)
        snake = Snake(start=(5, 5))
        snake.move('s')
        snake.move('w')
        assert snake.head() == (7, 5)
        
    def test_colisao_com_parede(self):
        snake = Snake(start=(0, 0), bounds=(10, 10))
        snake.move('a')
        assert snake.is_dead() == True
        snake = Snake(start=(0, 0), bounds=(10, 10))
        snake.move('w')
        assert snake.is_dead() == True
        snake = Snake(start=(10, 10), bounds=(10, 10))
        snake.move('d')
        assert snake.is_dead() == True
        snake = Snake(start=(10, 10), bounds=(10, 10))
        snake.move('s')
        assert snake.is_dead() == True

