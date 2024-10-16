import numpy as np
import pygame
from src.media.audio import load_beat_times

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
        density_grad = np.zeros((self.GRID_WIDTH, self.GRID_HEIGHT))
        opt_density_grad = np.ones((self.GRID_WIDTH, self.GRID_HEIGHT)) * OPT_DENSITY
        cx, cy = self.GRID_WIDTH // 2, self.GRID_HEIGHT // 2
        gravity_grad = np.zeros((self.GRID_WIDTH, self.GRID_HEIGHT))
        impulse_grad = np.zeros((self.GRID_WIDTH, self.GRID_HEIGHT))

def run_grid_sim():
    # CONSTANTS


    # LOAD BEAT TIMES
    audio_path = "audio/dreamtime.mp3"
    beat_times = load_beat_times(audio_path)

    # INIT GRID


    # Calculate gravity gradient
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            dist = np.sqrt((i - cx)**2 + (j - cy)**2) + 1
            gravity_grad[i, j] = GRAVITY_STRENGTH / dist

    # Calculate impulse gradient
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            dist = np.sqrt((i - cx)**2 + (j - cy)**2) + 1
            impulse_grad[i, j] = IMPULSE_STRENGTH / dist

    # Set initial optimal density to true
    opt_density_grad = opt_density_grad + gravity_grad

    # SET UP PYGAME
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Fluid Simulation (Density-Based Grid)')

    # START AUDIO
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()

    # MAIN SIMULATION LOOP
    clock = pygame.time.Clock()
    running = True
    current_beat_idx = 0
    density_grad[cx, cy] = GLOBAL_VOLUME
    while running:
        screen.fill((255, 255, 255))  # White background

        # CHECK FOR EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # CHECK FOR IMPULSE
        if current_beat_idx < len(beat_times):
            current_time = pygame.mixer.music.get_pos() / 1000.0  # Get time in seconds
            if current_time >= beat_times[current_beat_idx]:
                # APPLY IMPULSE TO OPTIMAL DENSITY
                density_grad = density_grad + impulse_grad
                current_beat_idx += 1

        # UPDATE DENSITY
        density_grad = density_grad + SURFACE_TENSION * (opt_density_grad - density_grad)

        # RENDER
        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                # Normalize the density to a value between 0 and 255
                color_intensity = int(min(max(density_grad[i,j],0), 255))

                # Draw the cell with the color mapped to the density
                color = (color_intensity, color_intensity, color_intensity)  # Shades of gray
                pygame.draw.rect(screen, color, (i*CELL_SIZE, j*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.display.flip()
        clock.tick(10)  # 60 FPS

    pygame.quit()