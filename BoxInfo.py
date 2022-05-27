import pygame
from pygame import Vector2


class BoxInfo:
    def __init__(self, grid_pos, box_sizes):
        self.sizes = box_sizes
        self.grid_pos = grid_pos
        self.real_pos = self._scale_grid_to_real_pos(grid_pos, box_sizes)
        self.box = pygame.Rect(self.real_pos, box_sizes)


    def update_box_position_by_grid(self, grid_pos):
        self.grid_pos = grid_pos
        self._update_real_pos()
        self._update_box()


    def _update_real_pos(self):
        self.real_pos.x = self.grid_pos.x * self.sizes.x
        self.real_pos.y = self.grid_pos.y * self.sizes.y


    def _update_box(self):
        self.box.update(self.real_pos, self.sizes)


    def _scale_grid_to_real_pos(self, grid_pos, sizes):
        return Vector2(grid_pos.x * sizes.x, grid_pos.y * sizes.y)
