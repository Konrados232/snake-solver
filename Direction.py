from enum import Enum
from pygame import Vector2


class Direction(Enum):
    UP = Vector2(0, -1)
    RIGHT = Vector2(1, 0)
    DOWN = Vector2(0, 1)
    LEFT = Vector2(-1, 0)


    @classmethod
    def get_counterclockwise(self, direction):
        if direction == Direction.UP:
            return Direction.LEFT
        elif direction == Direction.RIGHT:
            return Direction.UP
        elif direction == Direction.DOWN:
            return Direction.RIGHT
        elif direction == Direction.LEFT:
            return Direction.DOWN


    @classmethod
    def get_clockwise(self, direction):
        if direction == Direction.UP:
            return Direction.RIGHT
        elif direction == Direction.RIGHT:
            return Direction.DOWN
        elif direction == Direction.DOWN:
            return Direction.LEFT
        elif direction == Direction.LEFT:
            return Direction.UP
