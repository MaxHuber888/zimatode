import pygame
import math
from src.media.audio import load_beat_times
from src.particle.ParticleSim import ParticleSim
from src.branch.BranchSim import BranchSim
#from src.grid.GridSim import GridSim

# INITIALIZE PYGAME
pygame.init()

# GENERAL SIMULATION CONSTANTS
SCREEN_WIDTH, SCREEN_HEIGHT = 3840, 2160
FPS = 30
NAME = "Aphex Simulation"
SOUND_ON = True
IMPULSE_STRENGTH = 5
OBJECT_COLOR = (255, 255, 255)

# SIMULATION CONSTANTS
# "grid", "particle", "spring" or "branch"
SIMULATION_TYPE = "branch"

# RECORDING CONSTANTS
CAPTURING = False
CAPTURE_FPS = 30
MAX_FRAME_COUNT = 2000
_current_frame = 0

# CREATE SIMULATION OBJECT
match SIMULATION_TYPE:
    case "grid":
        pass
    case "particle":
        sim = ParticleSim(
            SCREEN_WIDTH=SCREEN_WIDTH,
            SCREEN_HEIGHT=SCREEN_HEIGHT,
            PARTICLE_COUNT=100,
            PARTICLE_COLLISIONS=False,
            PARTICLE_COLOR=OBJECT_COLOR
        )
    case "spring":
        pass
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

# LOAD BEAT TIMES
if SOUND_ON:
    audio_path = "audio/everything.mp3"
    beat_times = load_beat_times(audio_path)

    # START AUDIO
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()
current_beat_idx = 0

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

    # DETERMINE IMPULSE
    impulse = 0
    if SOUND_ON:
        if current_beat_idx < len(beat_times):
            current_time = pygame.mixer.music.get_pos() / 1000.0  # Get time in seconds
            if current_time >= beat_times[current_beat_idx]:
                impulse = IMPULSE_STRENGTH
                current_beat_idx += 1
    else:
        if current_beat_idx % 50 == 0:
            impulse = IMPULSE_STRENGTH
        current_beat_idx += 1


    # UPDATE SIMULATION
    sim.update(impulse=impulse)

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