import numpy as np
from src.particle.particle import Particle

class ParticleSim:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, PARTICLE_COUNT, PARTICLE_COLLISIONS,  PARTICLE_COLOR):
        # SET CONSTANTS
        self.PARTICLE_COUNT = PARTICLE_COUNT
        self.PARTICLE_COLLISIONS = PARTICLE_COLLISIONS
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.CENTER = np.array([SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2], dtype=float)
        self.PARTICLE_COLOR = PARTICLE_COLOR

        # INITIALIZE PARTICLES
        self.particles = [
            Particle(
                np.random.randint(0, SCREEN_WIDTH),
                np.random.randint(0, SCREEN_HEIGHT),
                self.PARTICLE_COLOR
            ) for _ in range(PARTICLE_COUNT)
        ]

    def update(self, impulse):
        # CALCULATE IMPULSE FOR PARTICLES
        if impulse > 0:
            impulse_direction = [particle.pos - self.CENTER for particle in self.particles]
            impulse_array = [direction / np.linalg.norm(direction) * impulse for direction in impulse_direction]
        else:
            impulse_array = [np.zeros(2) for _ in self.particles]

        # UPDATE PARTICLES
        for i, particle in enumerate(self.particles):
            if self.PARTICLE_COLLISIONS:
                # ADD COLLISION FORCE TO IMPULSE
                for j, other_particle in enumerate(self.particles):
                    if i != j and np.linalg.norm(particle.pos - other_particle.pos) < particle.PARTICLE_RADIUS + other_particle.PARTICLE_RADIUS:
                        impulse_array[i] += (particle.pos - other_particle.pos) / np.linalg.norm(particle.pos - other_particle.pos)

            # UPDATE PARTICLE
            particle.update(
                impulse=impulse_array[i],
                center=self.CENTER,
                screen_width=self.SCREEN_WIDTH,
                screen_height=self.SCREEN_HEIGHT
            )

    def draw(self, screen):
        # DRAW PARTICLES
        for i, particle in enumerate(self.particles):
            particle.draw(screen)