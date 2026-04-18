import pytest
from snake_screen import Snake

class TestSnakeCriacao:
    def test_snake_comeca_na_posicao_inicial(self):
        snake = Snake(start=(5, 5))
        assert snake.head() == (5, 5)

class TestSnakeMovimento:
    def test_mover_para_baixo(self):
        snake = Snake(start=(5,5))
        snake.move('s')
        assert snake.head() == (6, 5)

class TestSnakeColisao:
    def test_wrap_around_direita(self):
        snake = Snake(start=(5, 19), bounds=(20, 10), wrap=True)
        snake.move('d')
        assert snake.head() == (5, 0)

    def test_wrap_around_baixo(self):
        snake = Snake(start=(9, 5), bounds=(20, 10), wrap=True)
        snake.move('s')
        assert snake.head() == (0, 5)

    def test_colisao_com_o_proprio_corpo(self):
        snake = Snake(start=[(5, 5), (5, 4), (4, 4)])
        snake.move('a') 
        assert snake.is_dead() == True

    def test_nao_morre_ao_mover_para_cauda_que_sai(self):
        snake = Snake(start=[(5,5), (5,4), (4,4), (4,5)])
        snake.move('w') 
        assert snake.is_dead() == False

class TestGameLogic:
    def test_quantidade_de_frutas_base_inicial(self):
        snake = Snake(start=(0,0))
        # Lógica: (tamanho // 10) + 1
        assert (len(snake.body()) // 10) + 1 == 1

    def test_quantidade_de_frutas_tamanho_10(self):
        snake = Snake(start=[(0,i) for i in range(10)])
        assert (len(snake.body()) // 10) + 1 == 2
