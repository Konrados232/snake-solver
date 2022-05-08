import pygame
from pygame import Vector2
from collections import deque
import copy

from Direction import Direction
from PlayerPart import PlayerPart

class Player:
    def __init__(self, image, init_pos, size):
        self.image = image
        self.max_length = 100
        self.parts_queue = deque()
        for i in range(0, 10):
            a = PlayerPart(image, init_pos + Vector2(0, i), size)
            self.parts_queue.append(a)

    def move_one_step(self, direction):
        new_elem = self.parts_queue.popleft()
        new_elem.copy_pos_from(self.parts_queue[-1])
        new_elem.move_one_step(direction)
        self.parts_queue.append(new_elem)

    def get_player_part_queue(self):
        return self.parts_queue
