import pygame
class Branch:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, COLOR, BRANCHING_FACTOR, MAX_LEVELS, MAX_LENGTH, BRANCH_WIDTH, global_branches, pos, angle_deg, level=0, trunk=True, growing=True):
        # CONSTANTS
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.COLOR = COLOR
        self.BRANCHING_FACTOR = BRANCHING_FACTOR
        self.MAX_LEVELS = MAX_LEVELS
        self.MAX_LENGTH = MAX_LENGTH
        self.BRANCH_WIDTH = BRANCH_WIDTH

        self.global_branches = global_branches

        # SETUP
        self.growing = growing
        self.pos = pos
        self.angle_deg = angle_deg
        self.length = 0
        self.level = level
        self.trunk = trunk
        self.children = []
        self.prune = False

    def grow_and_shrink(self, growth, shrink):
        # GROWTH
        if growth > 0 and self.growing:
            # GROW
            self.length = min(self.length + growth, self.MAX_LENGTH)
        # IF MAX LENGTH REACHED
        if self.length == self.MAX_LENGTH:
            # BRANCH OUT
            self.growing = False
            if self.level < self.MAX_LEVELS and len(self.children) == 0:
                self.create_children()

        # SHRINKING
        if not self.growing and self.level == 0:
            # SHRINK
            self.length = max(self.length - shrink, 0)
        if not self.growing and self.level == 1 and not self.trunk:
            # SHRINK
            self.length = max(self.length - shrink, 0)

            # IF MIN LENGTH REACHED
            if self.length == 0:
                # DELETE
                self.prune = True
                for child in self.children:
                    child.level = child.level - 1

        # MOVE TOWARDS CENTER
        center = pygame.Vector2(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2)
        if self.pos != center:
            direction = (center - self.pos).normalize()
            self.pos += direction * shrink

        # MOVE CHILDREN
        for child in self.children:
            child.pos = self.pos + pygame.Vector2(self.length, 0).rotate(self.angle_deg)

    def create_children(self):
        for i in range(self.BRANCHING_FACTOR):
            child_angle_deg = self.angle_deg + 60 - i * 120 / (self.BRANCHING_FACTOR - 1)
            child_pos = self.pos + pygame.Vector2(self.length, 0).rotate(self.angle_deg)
            if i == 1 and self.trunk:
                child = Branch(
                    SCREEN_WIDTH=self.SCREEN_WIDTH,
                    SCREEN_HEIGHT=self.SCREEN_HEIGHT,
                    COLOR=self.COLOR,
                    BRANCHING_FACTOR=self.BRANCHING_FACTOR,
                    MAX_LEVELS=self.MAX_LEVELS,
                    MAX_LENGTH=self.MAX_LENGTH,
                    BRANCH_WIDTH=self.BRANCH_WIDTH,
                    global_branches=self.global_branches,
                    pos=child_pos,
                    angle_deg=child_angle_deg,
                    level=self.level + 1,
                    trunk=True
                )
                self.global_branches.append(child)
                self.children.append(child)
            else:
                child = Branch(
                    SCREEN_WIDTH=self.SCREEN_WIDTH,
                    SCREEN_HEIGHT=self.SCREEN_HEIGHT,
                    COLOR=self.COLOR,
                    BRANCHING_FACTOR=self.BRANCHING_FACTOR,
                    MAX_LEVELS=self.MAX_LEVELS,
                    MAX_LENGTH=self.MAX_LENGTH,
                    BRANCH_WIDTH=self.BRANCH_WIDTH,
                    global_branches=self.global_branches,
                    pos=child_pos,
                    angle_deg=child_angle_deg,
                    level=self.level + 1,
                    trunk=False
                )
                self.global_branches.append(child)
                self.children.append(child)

    def draw(self, surface):
        end_pos = self.pos + pygame.Vector2(self.length, 0).rotate(self.angle_deg)
        pygame.draw.line(surface, self.COLOR, self.pos, end_pos, int(self.BRANCH_WIDTH))
