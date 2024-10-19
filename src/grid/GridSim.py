import numpy as np
import pygame

class GridSim:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, SURFACE_TENSION=0.5, OPT_DENSITY=120, GRAVITY_STRENGTH=2, NUM_STEPS=5):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.CELL_SIZE = 10
        self.GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
        self.GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE
        self.GLOBAL_VOLUME = self.GRID_WIDTH * self.GRID_HEIGHT * 0.33
        self.SURFACE_TENSION = SURFACE_TENSION
        self.OPT_DENSITY = OPT_DENSITY
        self.GRAVITY_STRENGTH = GRAVITY_STRENGTH # How much higher can the density be at center
        self.NUM_STEPS = NUM_STEPS

        # INITIALIZE GRIDS
        self.density_grad = np.zeros((self.GRID_WIDTH, self.GRID_HEIGHT))
        self.opt_density_grad = np.ones((self.GRID_WIDTH, self.GRID_HEIGHT)) * OPT_DENSITY
        self.cx, self.cy = self.GRID_WIDTH // 2, self.GRID_HEIGHT // 2
        self.gravity_grad = np.zeros((self.GRID_WIDTH, self.GRID_HEIGHT))
        self.impulse_grad = np.zeros((self.GRID_WIDTH, self.GRID_HEIGHT))

        # Calculate gravity gradient
        for i in range(self.GRID_WIDTH):
            for j in range(self.GRID_HEIGHT):
                dist = np.sqrt((i - self.cx)**2 + (j - self.cy)**2) + 1
                self.gravity_grad[i, j] = GRAVITY_STRENGTH / dist

        # Set initial optimal density to true
        self.opt_density_grad = self.opt_density_grad + self.gravity_grad

        self.density_grad[self.cx, self.cy] = self.GLOBAL_VOLUME

    def update(self, low_impulse, mid_impulse, high_impulse, impulse):
        # Calculate impulse gradient
        for i in range(self.GRID_WIDTH):
            for j in range(self.GRID_HEIGHT):
                dist = np.sqrt((i - self.cx)**2 + (j - self.cy)**2) + 1
                self.impulse_grad[i, j] = impulse / dist

        # Update density gradient
        self.density_grad = self.density_grad + self.impulse_grad

        # Update optimal density gradient
        self.density_grad = self.density_grad + self.SURFACE_TENSION * (self.opt_density_grad - self.density_grad)

    def draw(self, surface):
        for i in range(self.GRID_WIDTH):
            for j in range(self.GRID_HEIGHT):
                # Normalize the density to a value between 0 and 255
                color_intensity = int(min(max(self.density_grad[i,j],0), 255))

                # Draw the cell with the color mapped to the density
                color = (color_intensity, color_intensity, color_intensity)  # Shades of gray
                pygame.draw.rect(surface, color, (i*self.CELL_SIZE, j*self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))


