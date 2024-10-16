class Point:
    def __init__(self, x, y, is_center=False):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.is_center = is_center

    def update(self, friction=0.98):
        if not self.is_center:
            self.x += self.vx
            self.y += self.vy
            self.vx *= friction
            self.vy *= friction