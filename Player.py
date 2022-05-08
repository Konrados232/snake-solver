import pygame
from pygame import Vector2
from collections import deque

from Direction import Direction
from PlayerPart import PlayerPart
from BoxInfo import BoxInfo

class Player:
    def __init__(self, image, init_pos, size):
        self.image = image
        self.max_length = 100
        self.parts_queue = deque()
        # for testing
        for i in range(0, 10):
            x = BoxInfo(init_pos + Vector2(0, i), size)
            a = PlayerPart(image, x)
            self.parts_queue.append(a)

  
    def move_one_step(self, direction):
        """Moves player by removing last element and adding new one to the head."""
        new_elem = self.parts_queue.popleft()
        new_elem.copy_box_info_from(self.parts_queue[-1].box_info)
        new_elem.move_one_step_in_grid(direction)
        self.parts_queue.append(new_elem)

    def get_player_part_queue(self):
        return self.parts_queue

    def get_current_head_pos(self):
        return self.parts_queue[-1].box_info.grid_pos
