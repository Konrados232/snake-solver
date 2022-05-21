import torch
import random

from RLModelInfo import RLModelInfo


class Agent:
    def __init__(self):
        self.rl_info = RLModelInfo(number_of_games=0, epsilon=0, gamma=0.5)



