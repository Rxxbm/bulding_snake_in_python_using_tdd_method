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
        
        # Colisão com o próprio corpo (ignora a ponta da cauda se não estiver crescendo)
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
        pass

    def display(self):
        pass
