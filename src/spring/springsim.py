import pygame
import math
import random

from src.media.audio  import load_beat_times
from src.spring.spring import Spring
from src.spring.point import Point


def run_spring_sim():
    # Initialize Pygame
    pygame.init()

    # Set up the display
    WIDTH, HEIGHT = 800, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Aphex Ferro Simulation")

    # Colors
    BLACK = (0, 0, 0)
    BLOB_COLOR = (100, 100, 255)
    BACK_BLOB_COLOR = (255, 100, 255)
    CENTER_COLOR = (255, 0, 0)

    # CONSTANTS
    NUM_POINTS = 40
    POINTS_PER_BULB = 5
    RADIUS = 150
    CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
    FRICTION = 0.96
    IMPULSE_STRENGTH = 30
    K = 0.001  # Spring constant
    EDGE_REST_LENGTH = 1

    # LOAD BEAT TIMES
    audio_path = "audio/everything.mp3"
    beat_times = load_beat_times(audio_path)

    # START AUDIO
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()

    center_point = Point(CENTER_X, CENTER_Y, is_center=True)
    springs = []

    def create_blob(RADIUS=RADIUS, NUM_POINTS=NUM_POINTS):
        points = []
        # Add initial edge point
        angle = 0
        x = CENTER_X + RADIUS * math.cos(angle)
        y = CENTER_Y + RADIUS * math.sin(angle)
        point = Point(x, y)
        points.append(point)
        springs.append(Spring(point, center_point, RADIUS, is_edge=False))

        for i in range(1,NUM_POINTS):
            # Create next point
            angle = 2 * math.pi * i / NUM_POINTS
            x = CENTER_X + RADIUS * math.cos(angle)
            y = CENTER_Y + RADIUS * math.sin(angle)
            point = Point(x, y)
            points.append(point)

            # Create edge spring to previous point
            prev_point = points[i-1]
            springs.append(Spring(point, prev_point, EDGE_REST_LENGTH))

            # Create center spring to this point
            springs.append(Spring(point, center_point, RADIUS, is_edge=False))

        # Create edge spring between first and last point
        last_point = points[-1]
        first_point = points[0]
        springs.append(Spring(first_point, last_point, EDGE_REST_LENGTH))

        return points

    # Create Top Blob
    blob_points = create_blob(100, NUM_POINTS*2)
    back_blob_points = create_blob(200, NUM_POINTS*2)

    def apply_impulse():
        counter = 0
        for p in blob_points + back_blob_points:
            if counter == 0:
                skew = random.uniform(0, 1)
                angle = math.atan2(p.y - CENTER_Y, p.x - CENTER_X)
                p.vx += IMPULSE_STRENGTH * math.cos(angle) * skew
                p.vy += IMPULSE_STRENGTH * math.sin(angle) * skew
            counter += 1
            if counter == POINTS_PER_BULB:
                counter = 0

    def draw_smooth_blob(surface, points, color, steps=1):
        if len(points) < 3:
            return

        smooth_points = []
        for i in range(len(points)):
            p0 = points[i]
            p1 = points[(i + 1) % len(points)]
            for j in range(steps):
                t = j / steps
                x = p0.x * (1 - t) + p1.x * t
                y = p0.y * (1 - t) + p1.y * t
                smooth_points.append((x, y))

        pygame.draw.polygon(surface, color, smooth_points)


    running = True
    clock = pygame.time.Clock()
    current_beat_idx = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                apply_impulse()

        # CHECK FOR IMPULSE
        if current_beat_idx < len(beat_times):
            current_time = pygame.mixer.music.get_pos() / 1000.0  # Get time in seconds
            if current_time >= beat_times[current_beat_idx]:
                # APPLY IMPULSE TO OPTIMAL DENSITY
                apply_impulse()
                current_beat_idx += 1

        for spring in springs:
            spring.update(friction=FRICTION, K=K)

        for point in blob_points:
            point.update()

        for point in back_blob_points:
            point.update()

        screen.fill(BLACK)
        draw_smooth_blob(screen, back_blob_points, BACK_BLOB_COLOR)
        draw_smooth_blob(screen, blob_points, BLOB_COLOR)
        pygame.draw.circle(screen, CENTER_COLOR, (int(center_point.x), int(center_point.y)), 5)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()