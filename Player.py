import pygame
from pygame import Vector2
from collections import deque

from Direction import Direction
from PlayerPart import PlayerPart

class Player:
    def __init__(self, image, init_pos, size):
        self.max_length = 100
        a = PlayerPart(image, init_pos, size)
        b = PlayerPart(image, init_pos + Vector2(0, 1), size)
        c = PlayerPart(image, init_pos + Vector2(0, 2), size)
        self.parts_queue = deque([a,b,c])

    def move_one_step(self, direction):
        last_elem = self.parts_queue.popleft()
        self.parts_queue.append(last_elem)
        for i in self.parts_queue:
            i.move_one_step(direction)

    def get_player_part_queue(self):
        return self.parts_queue
