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
        assert snake.head() == (6, 5) 
    def test_mover_para_direita(self):
        snake = Snake(start=(5,5))
        snake.move('d')
        assert snake.head() == (5, 6)
    def test_mover_para_esquerda(self):
        snake = Snake(start=(5,5))
        snake.move('a')
        assert snake.head() == (5, 4)
    def test_mover_para_cima(self):
        snake = Snake(start=(5,5))
        snake.move('w')
        assert snake.head() == (4, 5)
    def test_corpo_segue_cabeca(self):
        snake = Snake(start=(5,5))
        snake.grow()
        snake.move('d')
        assert snake.body() == [(5, 6), (5, 5)]

class TestSnakeColisao:
    def test_wrap_around_direita(self):
        snake = Snake(start=(5, 19), bounds=(20, 10), wrap=True)
        snake.move('d')
        assert snake.head() == (5, 0)
        assert snake.is_dead() == False

    def test_wrap_around_esquerda(self):
        snake = Snake(start=(5, 0), bounds=(20, 10), wrap=True)
        snake.move('a')
        assert snake.head() == (5, 19)

    def test_wrap_around_baixo(self):
        snake = Snake(start=(9, 5), bounds=(20, 10), wrap=True)
        snake.move('s')
        assert snake.head() == (0, 5)

    def test_wrap_around_cima(self):
        snake = Snake(start=(0, 5), bounds=(20, 10), wrap=True)
        snake.move('w')
        assert snake.head() == (9, 5)

    def test_nao_pode_inverter_direcao(self):
        snake = Snake(start=(5, 5))
        snake.move('d')
        snake.move('a')
        assert snake.head() == (5, 7)
        
    def test_colisao_com_parede(self):
        snake = Snake(start=(0, 0), bounds=(10, 10))
        snake.move('a')
        assert snake.is_dead() == True
    
    def test_colisao_com_o_proprio_corpo(self):
        snake = Snake(start=[(5, 5), (5, 4), (4, 4)])
        snake.move('a') 
        assert snake.is_dead() == True

    def test_colisao_corpo_dinamicamente(self):
        snake = Snake(start=(5, 5))
        for _ in range(4):
            snake.grow()
        snake.move('d') # (5, 6)
        snake.move('s') # (6, 6)
        snake.move('a') # (6, 5)
        snake.move('w') # (5, 5)
        assert snake.is_dead() == True

class TestGameLogic:
    def test_quantidade_de_frutas_base_inicial(self):
        snake = Snake(start=(0,0))
        assert (len(snake.body()) // 10) + 1 == 1

    def test_quantidade_de_frutas_tamanho_10(self):
        snake = Snake(start=[(0,i) for i in range(10)])
        assert (len(snake.body()) // 10) + 1 == 2

    def test_quantidade_de_frutas_tamanho_20(self):
        snake = Snake(start=[(0,i) for i in range(20)])
        assert (len(snake.body()) // 10) + 1 == 3

    def test_comer_uma_das_várias_frutas(self):
        snake = Snake(start=(5,5))
        frutas = [(5,6), (1,1)]
        snake.move('d')
        assert snake.head() in frutas
