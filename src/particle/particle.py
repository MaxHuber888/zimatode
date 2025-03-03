import numpy as np
import pygame

class Particle:
    def __init__(self, X, Y, COLOR):
        self.pos = np.array([X, Y], dtype=float)
        self.vel = np.zeros(2)

        # CONSTANTS
        self.BOUNDED = False
        self.PARTICLE_RADIUS = 3
        self.PLANET_RADIUS = 20
        self.HARD_PLANET = True
        self.COLOR = COLOR

    def update(self, impulse, center, screen_width=1600, screen_height=1200):
        # Fluid Friction
        self.vel *= 0.99

        # Get direction and distance to center
        direction_to_center = center - self.pos
        distance_to_center = np.linalg.norm(direction_to_center)

        # Attraction toward the center
        if distance_to_center > 0:
            force_toward_center = 0.5 * direction_to_center / distance_to_center  # Attraction force
            self.vel += force_toward_center

        # If on planet suppress gravity
        if self.HARD_PLANET:
            if distance_to_center < self.PLANET_RADIUS:
                self.vel *= 0

        # Apply impulse if there is one
        self.vel += impulse

        # Update position based on velocity
        self.pos += self.vel

        # Boundary check: particles bounce off walls
        if self.BOUNDED:
            if self.pos[0] <= 0 or self.pos[0] >= screen_width:
                self.vel[0] *= -1
            if self.pos[1] <= 0 or self.pos[1] >= screen_height:
                self.vel[1] *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, self.COLOR, self.pos.astype(int), self.PARTICLE_RADIUS)