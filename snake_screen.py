import os
import sys
import tty
import termios
import threading
import time
import random

class Snake:
    def __init__(self, start, bounds=(10,10), wrap=False):
        if isinstance(start, list):
            self._body = list(start)
        else:
            self._body = [start]
        self.grow_pending = 0
        self.current_dir = ''
        self.dead = False
        self.bounds = bounds
        self.wrap = wrap

    def is_dead(self):
        return self.dead

    def head(self):
        return self._body[0]

    def body(self):
        return list(self._body)
    
    def grow(self):
        self.grow_pending += 1

    def move(self, direction):
        r, c = self.head()
        opposites = {'w': 's', 's': 'w', 'a':'d', 'd':'a'}
        if self.current_dir and direction == opposites.get(self.current_dir):
            direction = self.current_dir

        if direction == 's': r += 1
        elif direction == 'w': r -= 1
        elif direction == 'a': c -= 1
        elif direction == 'd': c += 1

        if self.wrap:
            c = c % self.bounds[0]
            r = r % self.bounds[1]
        else:
            if (c < 0 or c >= self.bounds[0]) or (r < 0 or r >= self.bounds[1]):
                self.dead = True
                return
        
        new_head = (r, c)
        check_body = self._body if self.grow_pending > 0 else self._body[:-1]
        if new_head in check_body:
            self.dead = True
            return

        self.current_dir = direction
        self._body.insert(0, new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self._body.pop()

class io_handler:
    def __init__(self, dim, speed):
        self.x_size = dim[0]
        self.y_size = dim[1]
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

    def update_state(self, snake, fruits):
        for r in range(self.y_size):
            for c in range(self.x_size): self.matrix[r][c] = 0
        for fr, fc in fruits:
            if 0 <= fr < self.y_size and 0 <= fc < self.x_size: self.matrix[fr][fc] = 3
        for i, (r, c) in enumerate(snake.body()):
            if 0 <= r < self.y_size and 0 <= c < self.x_size: self.matrix[r][c] = 2 if i == 0 else 1

    def display(self, snake, fruits):
        output = "\033[H"
        h_line = "+" + "--" * self.x_size + "+\r\n"
        output += h_line
        for line in self.matrix:
            row = "|"
            for item in line:
                if item == 1: row += "[]"
                elif item == 2: row += "<>"
                elif item == 3: row += "()"
                else: row += "  "
            output += row + "|\r\n"
        output += h_line
        output += f"SCORE: {len(snake.body())-1} | TECLA: {self.last_input.upper()}\r\n"
        sys.stdout.write(output)
        sys.stdout.flush()

def spawn_fruit(snake, fruits, bounds):
    while True:
        r, c = random.randint(0, bounds[1]-1), random.randint(0, bounds[0]-1)
        if (r, c) not in snake.body() and (r, c) not in fruits: return (r, c)

def main():
    DIM = (20, 10)
    screen = io_handler(DIM, 0.15)
    snake = Snake(start=(DIM[1]//2, DIM[0]//2), bounds=DIM, wrap=True)
    fruits = [spawn_fruit(snake, [], DIM)]
    screen.record_inputs()
    sys.stdout.write("\033[2J\033[?25l")
    try:
        while True:
            if screen.last_input == 'end': break
            snake.move(screen.last_input)
            if snake.is_dead(): break
            if snake.head() in fruits:
                snake.grow()
                fruits.remove(snake.head())
            while len(fruits) < (len(snake.body()) // 10) + 1:
                fruits.append(spawn_fruit(snake, fruits, DIM))
            screen.update_state(snake, fruits)
            screen.display(snake, fruits)
            time.sleep(screen.game_speed)
    finally:
        sys.stdout.write("\033[?25h\r\nGAME OVER\r\n")

if __name__ == '__main__':
    main()
