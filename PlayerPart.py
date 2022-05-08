import pygame
from pygame import Vector2

from Direction import Direction

class PlayerPart:
    def __init__(self, image, grid_pos, sizes):
        self.image = image
        self.sizes = sizes
        self.grid_pos = grid_pos
        self.real_pos = self.scale_grid_to_real_pos(grid_pos, sizes)
        self.box = pygame.Rect(self.real_pos, sizes)

    def move_one_step(self, direction):
        self.update_grid_pos(direction)
        self.update_real_pos(direction)
        self.update_box()

    def update_grid_pos(self, direction):
        self.grid_pos.x += direction.value[0]
        self.grid_pos.y += direction.value[1]

    def update_real_pos(self, direction):
        self.real_pos.x += direction.value[0] * self.sizes.x
        self.real_pos.y += direction.value[1] * self.sizes.y

    def update_box(self):
        self.box.update(self.real_pos, self.sizes)

    def scale_grid_to_real_pos(self, grid_pos, sizes):
        return Vector2(grid_pos.x * sizes.x, grid_pos.y * sizes.y)