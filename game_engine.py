import random
from snake import Snake

class GameEngine:
    def __init__(self, bounds=(20, 10), wrap=True):
        self.bounds = bounds
        start_pos = (bounds[1]//2, bounds[0]//2)
        self.snake = Snake(start=start_pos, bounds=bounds, wrap=wrap)
        self.fruits = []
        self._spawn_required_fruits()

    def _spawn_required_fruits(self):
        target = (len(self.snake.body()) // 10) + 1
        while len(self.fruits) < target:
            r, c = random.randint(0, self.bounds[1]-1), random.randint(0, self.bounds[0]-1)
            if (r, c) not in self.snake.body() and (r, c) not in self.fruits:
                self.fruits.append((r, c))

    def update(self, direction):
        if self.snake.is_dead(): return
        self.snake.move(direction)
        if self.snake.head() in self.fruits:
            self.snake.grow()
            self.fruits.remove(self.snake.head())
        self._spawn_required_fruits()
