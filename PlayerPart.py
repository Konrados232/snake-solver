import pygame
import random
from pygame import Vector2

from Direction import Direction

class PlayerPart:
    def __init__(self, image, box_info):
        self.image = image
        self.box_info = box_info

    def copy_box_info_from(self, box_info):
        self.box_info.grid_pos = box_info.grid_pos
        self.box_info.real_pos = box_info.real_pos
        self.box_info.sizes = box_info.sizes

    def move_one_step_in_grid(self, direction):
        new_grid_pos = Vector2(self.box_info.grid_pos.x + direction.value[0], self.box_info.grid_pos.y + direction.value[1])
        self.color_randomly_rect()
        self.box_info.update_box_position_by_grid(new_grid_pos)

    def get_grid_pos(self):
        return self.box_info.grid_pos

    def color_randomly_rect(self):
        self.image.fill((random.randint(50,250),random.randint(50,250),random.randint(50,250)))

    def scale_grid_to_real_pos(self, grid_pos, sizes):
        return Vector2(grid_pos.x * sizes.x, grid_pos.y * sizes.y)
    