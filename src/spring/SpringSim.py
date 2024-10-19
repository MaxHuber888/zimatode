import pygame
import math
import random
from src.spring.spring import Spring
from src.spring.point import Point

class SpringSim():
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, NUM_POINTS, POINTS_PER_BULB, RADIUS=200, FRICTION=0.96, K=0.00001, EDGE_REST_LENGTH=1):
        # SETUP CONSTANTS
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.NUM_POINTS = NUM_POINTS
        self.POINTS_PER_BULB = POINTS_PER_BULB
        self.RADIUS = RADIUS
        self.CENTER_X, self.CENTER_Y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        self.FRICTION = FRICTION
        self.K = K  # Spring constant
        self.EDGE_REST_LENGTH = EDGE_REST_LENGTH

        self.points = []
        self.springs = []

        # Create Center Point
        self.center_point = Point(self.CENTER_X, self.CENTER_Y, is_center=True)

        # Create Blobs
        self.points.append(self.create_blob(RADIUS, NUM_POINTS))
        self.points.append(self.create_blob(2*RADIUS/3, NUM_POINTS))
        self.points.append(self.create_blob(RADIUS/3, NUM_POINTS))

    def update(self, low_impulse, mid_impulse, high_impulse, impulse):
        # Apply impulse
        self.apply_impulse(low_impulse, self.points[0])
        self.apply_impulse(mid_impulse, self.points[1])
        self.apply_impulse(high_impulse, self.points[2])

        # Update springs
        for spring in self.springs:
            spring.update(friction=self.FRICTION, K=self.K)

        # Update points
        for blob in self.points:
            for p in blob:
                p.update(friction=self.FRICTION)

    def draw(self, surface):
        for i, blob in enumerate(self.points):
            self.draw_smooth_blob(surface=surface, points=blob, color=(155/len(self.points)*(len(self.points)-i)+100, 255, 255), steps=2)

    def create_blob(self, radius, num_points):
        points = []
        # Add initial edge point
        angle = 0
        x = self.CENTER_X + radius * math.cos(angle)
        y = self.CENTER_Y + radius * math.sin(angle)
        point = Point(x, y)
        points.append(point)
        self.springs.append(Spring(point, self.center_point, radius, is_edge=False))

        for i in range(1, num_points):
            # Create next point
            angle = 2 * math.pi * i / num_points
            x = self.CENTER_X + radius * math.cos(angle)
            y = self.CENTER_Y + radius * math.sin(angle)
            point = Point(x, y)
            points.append(point)

            # Create edge spring to previous point
            prev_point = points[i-1]
            self.springs.append(Spring(point, prev_point, self.EDGE_REST_LENGTH))

            # Create center spring to this point
            self.springs.append(Spring(point, self.center_point, radius, is_edge=False))

        # Create edge spring between first and last point
        last_point = points[-1]
        first_point = points[0]
        self.springs.append(Spring(first_point, last_point, self.EDGE_REST_LENGTH))

        return points

    def apply_impulse(self, impulse, blob):
        counter = 0
        for p in blob:
            if counter == 0:
                skew = random.uniform(0, 1)
                angle = math.atan2(p.y - self.CENTER_Y, p.x - self.CENTER_X)
                p.vx += impulse * math.cos(angle) * skew
                p.vy += impulse * math.sin(angle) * skew
            counter += 1
            if counter == self.POINTS_PER_BULB:
                counter = 0

    def draw_smooth_blob(self,surface, points, color, steps=1):
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