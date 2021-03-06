from pygame import Vector2
from collections import deque

from Direction import Direction
from PlayerPart import PlayerPart
from BoxInfo import BoxInfo
from Direction import Direction


class Player:
    def __init__(self, image, init_pos, size):
        self.image = image
        self.max_length = 100
        self.image = image # to reconsider
        self.size = size # to reconsider
        self.parts_queue = deque()
        self.init_pos = init_pos
        self.current_direction = Direction.RIGHT
        for i in range(0, 10):
            x = BoxInfo(init_pos + Vector2(0, i), size)
            a = PlayerPart(image, x)
            self.parts_queue.append(a)

        self.tailing_pos = init_pos + Vector2(0,0)

    def reset(self):
        self.parts_queue = deque()
        self.current_direction = Direction.RIGHT
        for i in range(0, 10):
            x = BoxInfo(self.init_pos + Vector2(0, i), self.size)
            a = PlayerPart(self.image, x)
            self.parts_queue.append(a)

        self.tailing_pos = self.init_pos + Vector2(0,0)

  
    def move_one_step(self, direction):
        """Moves player by removing last element and adding new one to the head."""
        self.update_tailing_pos() # needs to be executed before changing any other position
        new_elem = self.parts_queue.popleft()
        new_elem.copy_box_info_from(self.parts_queue[-1].box_info)
        new_elem.move_one_step_in_grid(direction)
        self.parts_queue.append(new_elem)

        self.update_curr_dir(direction)

    def update_tailing_pos(self):
        self.tailing_pos.update(self.parts_queue[0].get_grid_pos())

    def increase_in_size_by_one(self):
        new_box = BoxInfo(self.tailing_pos, self.size)
        new_elem = PlayerPart(self.image, new_box)

        self.parts_queue.appendleft(new_elem)


    def update_curr_dir(self, direct):
        self.current_direction = direct

    def get_current_direction(self):
        return self.current_direction

    def get_player_part_queue(self):
        return self.parts_queue

    def get_current_head_pos(self):
        return self.parts_queue[-1].get_grid_pos()
