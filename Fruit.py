import random
from pygame import Vector2

from BoxInfo import BoxInfo

class Fruit:
    def __init__(self, image, init_pos, size):
        self.init_pos = init_pos
        self.size = size
        self.image = image
        self.box_info = BoxInfo(init_pos, size)


    def reset(self):
        self.image = self.image
        self.box_info = BoxInfo(self.init_pos, self.size)


    def set_random_pos(self, restricted_pos, grid_sizes):
        new_grid_pos = self._generate_next_pos(restricted_pos, grid_sizes)

        self.box_info.update_box_position_by_grid(new_grid_pos)
    

    def _generate_next_pos(self, restricted_pos, grid_sizes):
        next_pos = Vector2(random.randint(0, grid_sizes[0] - 1), random.randint(0, grid_sizes[1] - 1))
        if self.is_occupied(next_pos, restricted_pos):
            return self._generate_next_pos(restricted_pos, grid_sizes)
        else:
            return next_pos


    def is_occupied(self, generated_pos, restricted_pos):
        for pos in restricted_pos:
            if generated_pos.x == pos.get_grid_pos().x and generated_pos.y == pos.get_grid_pos().y:
                return True
        
        return False


    def get_fruit_pos(self):
        return self.box_info.grid_pos


    def scale_grid_to_real_pos(self, grid_pos, sizes):
        return Vector2(grid_pos.x * sizes.x, grid_pos.y * sizes.y)
