from dataclasses import dataclass

@dataclass
class RLModelInfo:
    number_of_games: int
    epsilon: float
    gamma: float
    