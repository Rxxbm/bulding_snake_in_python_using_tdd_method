import pytest
from snake import Snake
from game_engine import GameEngine

class TestGameEngine:
    def test_engine_inicializa_com_uma_fruta(self):
        engine = GameEngine(bounds=(20, 10))
        assert len(engine.fruits) == 1
        assert not engine.snake.is_dead()

    def test_engine_aumenta_frutas_ao_atingir_score_10(self):
        # Inicializa a engine e simula a cobra já tendo tamanho 10
        engine = GameEngine(bounds=(20, 10))
        # Criamos uma cobra com 10 segmentos
        engine.snake._body = [(0,i) for i in range(10)]
        engine.update('d') # Faz a cobra se mover e checar as regras
        assert len(engine.fruits) == 2

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

    def test_colisao_com_o_proprio_corpo(self):
        snake = Snake(start=[(5, 5), (5, 4), (4, 4)])
        snake.move('a') 
        assert snake.is_dead() == True

    def test_nao_morre_ao_mover_para_cauda_que_sai(self):
        snake = Snake(start=[(5,5), (5,4), (4,4), (4,5)])
        snake.move('w') 
        assert snake.is_dead() == False
