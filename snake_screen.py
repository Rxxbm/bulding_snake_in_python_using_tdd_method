import os
import sys
import tty
import termios
import threading
import time
from game_engine import GameEngine

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
            if 0 <= r < self.y_size and 0 <= c < self.x_size:
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
