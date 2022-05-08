import pygame
from pygame import Vector2


class Fruit:
    def __init__(self, image, box_info):
        self.image = image
        self.box_info = box_info

    def scale_grid_to_real_pos(self, grid_pos, sizes):
        return Vector2(grid_pos.x * sizes.x, grid_pos.y * sizes.y)
    