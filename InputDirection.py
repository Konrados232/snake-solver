from enum import Enum


class InputDirection(Enum):
    FORWARD = [1,0,0]
    TURN_CLOCKWISE = [0,1,0]
    TURN_COUNTERCLOCKWISE = [0,0,1]
