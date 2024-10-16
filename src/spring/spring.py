import math


class Spring:
    def __init__(self, p1, p2, rest_length, is_edge=True):
        self.p1 = p1
        self.p2 = p2
        self.rest_length = rest_length
        self.length = self.calculate_length()
        self.is_edge = is_edge

    def calculate_length(self):
        dx = self.p2.x - self.p1.x
        dy = self.p2.y - self.p1.y
        return math.sqrt(dx*dx + dy*dy)

    def update(self, friction=0.98, K=0.001):
        # Get current length and velocity
        self.length = self.calculate_length()

        # Calculate spring force
        force = 0
        if self.length > self.rest_length:
            force = K * (self.length - self.rest_length)
        elif self.length < self.rest_length:
            force = -K * (self.rest_length - self.length)

        # Apply correction force to points
        dx = self.p2.x - self.p1.x
        dy = self.p2.y - self.p1.y

        self.p1.vx += force * dx
        self.p1.vy += force * dy
        self.p2.vx -= force * dx
        self.p2.vy -= force * dy




