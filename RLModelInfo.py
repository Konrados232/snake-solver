from dataclasses import dataclass


@dataclass
class RLModelInfo:
    number_of_games: int
    epsilon: float
    gamma: float
    learning_rate: float
    input_vector_size: int
    output_vector_size: int
    number_of_layers: int
    layer_sizes: list
    maximum_memory: int
    batch_size: int
    number_of_games_for_training: int
    random_scale: int
    