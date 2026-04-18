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
