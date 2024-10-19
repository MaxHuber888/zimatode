import pygame
import math
from src.branch.branch import Branch

class BranchSim():
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, MAX_LENGTH, BRANCHING_FACTOR, GROWTH_RATE, SHRINK_RATE, BRANCH_WIDTH, MAX_LEVELS, BRANCH_COLOR):
        # SETUP CONSTANTS
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.MAX_LENGTH = MAX_LENGTH
        self.BRANCHING_FACTOR = BRANCHING_FACTOR
        self.GROWTH_RATE = GROWTH_RATE
        self.SHRINK_RATE = SHRINK_RATE
        self.BRANCH_WIDTH = BRANCH_WIDTH
        self.MAX_LEVELS = MAX_LEVELS
        self.BRANCH_COLOR = BRANCH_COLOR
        self.CENTER = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        self.branches = []
        for i in range(BRANCHING_FACTOR):
            angle_deg = i * 360 / BRANCHING_FACTOR
            self.branches.append(Branch(
                SCREEN_WIDTH=self.SCREEN_WIDTH,
                SCREEN_HEIGHT=self.SCREEN_HEIGHT,
                COLOR=self.BRANCH_COLOR,
                BRANCHING_FACTOR=self.BRANCHING_FACTOR,
                MAX_LEVELS=self.MAX_LEVELS,
                MAX_LENGTH=self.MAX_LENGTH,
                BRANCH_WIDTH=self.BRANCH_WIDTH,
                global_branches=self.branches,
                pos=self.CENTER,
                angle_deg=angle_deg,
                level=0,
                trunk=True
            ))

    def update(self, low_impulse, mid_impulse, high_impulse, impulse):
        for branch in self.branches:
            branch.grow_and_shrink(self.GROWTH_RATE + impulse, self.SHRINK_RATE)

    def draw(self, surface):
        for branch in self.branches:
            branch.draw(surface)
