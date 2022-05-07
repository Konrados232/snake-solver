import pygame

from Direction import Direction

class Player:
    def __init__(self, image, init_pos, size):
        self.image = image
        self.box = pygame.Rect(init_pos, size)
        self.step_length = 10


    def move_one_step(self, direction):
        x_pos = direction.value[0] * self.step_length
        y_pos = direction.value[1] * self.step_length
        self.box = self.box.move(x_pos, y_pos)


