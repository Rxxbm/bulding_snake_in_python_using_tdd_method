import os
import sys
import tty
import termios
import threading
import time

class Snake:
    def __init__(self, start):
        self._body = [start]
        self.grow_pending = 0
        self.current_dir = ''

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

        if direction == 's':
            r += 1
        elif direction == 'w':
            r -= 1
        elif direction == 'a':
            c -= 1
        elif direction == 'd':
            c += 1
        
        self.current_dir = direction

        new_head = (r, c)
        
        self._body.insert(0, new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self._body.pop()

class io_handler:

    x_size: int
    y_size: int
    game_speed: float
    last_input: str

    def __init__(self, dim, speed):
        self.x_size = dim[0]
        self.y_size = dim[1]
        self.game_speed = speed
        self.last_input = 'w'
        self.matrix = [[0] * self.x_size for _ in range(self.y_size)]

    def record_inputs(self):
        def read_keys():
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                while True:
                    ch = sys.stdin.read(1)
                    if ch in ('w', 'a', 's', 'd'):
                        self.last_input = ch
                    elif ch == '\x1b':
                        self.last_input = 'end'
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)

        t = threading.Thread(target=read_keys, daemon=True)
        t.start()

    def display(self):
        def display_h_line(self):
            print ('+', end='')
            print ('--'* len(self.matrix[0]), end='')
            print ('+')
        
        def display_content_line(line):
            print ('|', end='')
            for item in line: 
                if item == 1:
                    print ('[]', end='')
                elif item == 2:
                    print ('<>', end='')
                elif item == 3:
                    print ('()', end='')
                else:
                    print ('  ', end='')

            print ('|')

        os.system('cls' if os.name == 'nt' else 'clear')
        display_h_line(self)
        for line in self.matrix:
            display_content_line(line)
        display_h_line(self)

### exemplo do uso da classe io_handler
if __name__ == '__main__':
    instance = io_handler((10,15), 0.5)
    instance.matrix[0][0] = 1 #corpo
    instance.matrix[0][1] = 2 #cabeça
    instance.matrix[0][2] = 3 #fruta

    def game_loop():
        instance.record_inputs()
        while True:
            instance.display()
            print("mova com WASD, saia com esc. Ultimo botão:", end=' ')
            ###adicione seu código para lidar com o jogo aqui

            print(instance.last_input)
            if(instance.last_input == 'end'):
                exit()
            time.sleep(instance.game_speed)

    game_loop()
