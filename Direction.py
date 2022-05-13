from enum import Enum


class Direction(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)

    # tbh, I don't know better method without overcomplicating
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