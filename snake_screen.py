import os
import sys
import tty
import termios
import threading
import time
import random

class Snake:
    def __init__(self, start, bounds=(10,10), wrap=False):
        self._body = [start] if not isinstance(start, list) else list(start)
        self.grow_pending = 0
        self.current_dir = ''
        self.dead = False
        self.bounds = bounds
        self.wrap = wrap

    def is_dead(self): return self.dead
    def head(self): return self._body[0]
    def body(self): return list(self._body)
    def grow(self): self.grow_pending += 1

    def move(self, direction):
        if not direction: return
        r, c = self.head()
        opposites = {'w': 's', 's': 'w', 'a':'d', 'd':'a'}
        if self.current_dir and direction == opposites.get(self.current_dir): direction = self.current_dir
        if direction == 's': r += 1
        elif direction == 'w': r -= 1
        elif direction == 'a': c -= 1
        elif direction == 'd': c += 1
        if self.wrap:
            c, r = c % self.bounds[0], r % self.bounds[1]
        elif (c < 0 or c >= self.bounds[0]) or (r < 0 or r >= self.bounds[1]):
            self.dead = True
            return
        new_head = (r, c)
        check_body = self._body if self.grow_pending > 0 else self._body[:-1]
        if new_head in check_body:
            self.dead = True
            return
        self.current_dir = direction
        self._body.insert(0, new_head)
        if self.grow_pending > 0: self.grow_pending -= 1
        else: self._body.pop()

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

class io_handler:
    def __init__(self, dim, speed):
        self.x_size, self.y_size = dim
        self.game_speed = speed
        self.last_input = 'd'
        self.matrix = [[0] * self.x_size for _ in range(self.y_size)]

    def record_inputs(self):
        def read_keys():
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                while True:
                    ch = sys.stdin.read(1)
                    if ch in ('w', 'a', 's', 'd'): self.last_input = ch
                    elif ch == '\x1b':
                        self.last_input = 'end'
                        break
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
        t = threading.Thread(target=read_keys, daemon=True)
        t.start()

    def sync_and_display(self, engine):
        for r in range(self.y_size):
            for c in range(self.x_size): self.matrix[r][c] = 0
        for fr, fc in engine.fruits: self.matrix[fr][fc] = 3
        for i, (r, c) in enumerate(engine.snake.body()):
            self.matrix[r][c] = 2 if i == 0 else 1
        output = "\033[H" + "+" + "--" * self.x_size + "+\r\n"
        for line in self.matrix:
            row = "|"
            for item in line:
                if item == 1: row += "[]"
                elif item == 2: row += "<>"
                elif item == 3: row += "()"
                else: row += "  "
            output += row + "|\r\n"
        output += "+" + "--" * self.x_size + "+\r\n"
        output += f"SCORE: {len(engine.snake.body())-1} | TECLA: {self.last_input.upper()}\r\n"
        sys.stdout.write(output)
        sys.stdout.flush()

def main():
    DIM = (20, 10)
    engine = GameEngine(bounds=DIM)
    io = io_handler(DIM, 0.15)
    io.record_inputs()
    sys.stdout.write("\033[2J\033[?25l")
    try:
        while not engine.snake.is_dead():
            if io.last_input == 'end': break
            engine.update(io.last_input)
            io.sync_and_display(engine)
            time.sleep(io.game_speed)
    finally:
        sys.stdout.write("\033[?25h\r\nGAME OVER\r\n")

if __name__ == '__main__': main()
