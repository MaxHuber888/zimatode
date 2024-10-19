import pygame
import math
from src.media.audio import analyze_audio, get_current_energy
from src.particle.ParticleSim import ParticleSim
from src.branch.BranchSim import BranchSim
from src.grid.GridSim import GridSim
from src.spring.SpringSim import SpringSim

# INITIALIZE PYGAME
pygame.init()

# GENERAL SIMULATION CONSTANTS
SCREEN_WIDTH, SCREEN_HEIGHT = 3840, 2160
FPS = 30
NAME = "Aphex Simulation"
SOUND_ON = True
OBJECT_COLOR = (255, 255, 255)

# IMPULSE CONSTANTS
BASE_IMPULSE_STRENGTH = 10
ENERGY_THRESHOLD = 0.2  # Minimum energy level to trigger impulse

# SIMULATION CONSTANTS
SIMULATION_TYPE = "spring"  # "grid", "particle", "spring" or "branch"

# RECORDING CONSTANTS
CAPTURING = False
CAPTURE_FPS = 30
MAX_FRAME_COUNT = 2000
_current_frame = 0

# CREATE SIMULATION OBJECT
match SIMULATION_TYPE:
    case "grid":
        sim = GridSim(
            SCREEN_WIDTH=SCREEN_WIDTH,
            SCREEN_HEIGHT=SCREEN_HEIGHT,
            CELL_SIZE=10,
            SURFACE_TENSION=0.5,
            OPT_DENSITY=120,
            GRAVITY_STRENGTH=2,
            NUM_STEPS=5
        )
    case "particle":
        sim = ParticleSim(
            SCREEN_WIDTH=SCREEN_WIDTH,
            SCREEN_HEIGHT=SCREEN_HEIGHT,
            PARTICLE_COUNT=100,
            PARTICLE_COLLISIONS=False,
            PARTICLE_COLOR=OBJECT_COLOR
        )
    case "spring":
        sim = SpringSim(
            SCREEN_WIDTH=SCREEN_WIDTH,
            SCREEN_HEIGHT=SCREEN_HEIGHT,
            NUM_POINTS=100,
            POINTS_PER_BULB=5,
            RADIUS=300,
            FRICTION=0.96,
            K=0.001,
            EDGE_REST_LENGTH=1
        )
    case "branch":
        sim = BranchSim(
            SCREEN_WIDTH=SCREEN_WIDTH,
            SCREEN_HEIGHT=SCREEN_HEIGHT,
            MAX_LENGTH=200,
            BRANCHING_FACTOR=6,
            GROWTH_RATE=0.3,
            SHRINK_RATE=0.3,
            BRANCH_WIDTH=1,
            MAX_LEVELS=5,
            BRANCH_COLOR=OBJECT_COLOR
        )

# LOAD AUDIO ANALYSIS
if SOUND_ON:
    audio_path = "audio/half.mp3"
    _, energies = analyze_audio(audio_path)

    # START AUDIO
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()

# MAIN GAME LOOP
running = True
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(NAME)

while running:
    # HANDLE EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            running = False

    # DETERMINE IMPULSES
    low_impulse, mid_impulse, high_impulse, impulse = 0, 0, 0, 0
    if SOUND_ON:
        current_time = pygame.mixer.music.get_pos() / 1000.0  # Get time in seconds
        low_impulse, mid_impulse, high_impulse, impulse = get_current_energy(
            current_time, energies, ENERGY_THRESHOLD, BASE_IMPULSE_STRENGTH
        )
    else:
        # Demo mode - create periodic impulses
        frame_count = pygame.time.get_ticks() // 33  # approximately 30 FPS
        if frame_count % 50 == 0:
            low_impulse = BASE_IMPULSE_STRENGTH
            mid_impulse = BASE_IMPULSE_STRENGTH
            high_impulse = BASE_IMPULSE_STRENGTH
            impulse = BASE_IMPULSE_STRENGTH

    # UPDATE SIMULATION
    sim.update(low_impulse, mid_impulse, high_impulse, impulse)

    # DRAW SIMULATION
    screen.fill((0, 0, 0))
    sim.draw(screen)

    # IF CAPTURING, SAVE FRAME
    if CAPTURING:
        pygame.image.save(screen, f"capture/frame_{_current_frame}.png")
        _current_frame += 1

        # Prevent endless capture
        if _current_frame == MAX_FRAME_COUNT:
            CAPTURING = False
            print("Exceeded maximum frame count. Capturing stopped.")

    # UPDATE DISPLAY
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()