from asyncio import current_task
from configparser import RawConfigParser
from http.client import ImproperConnectionState
from typing import Dict, final
import torch
import numpy as np
import random

from pygame import Vector2
from RLModelInfo import RLModelInfo
from Game import Game
from collections import deque
from Direction import Direction



class Agent:
    def __init__(self):
        self.rl_info = RLModelInfo(number_of_games=0, epsilon=0, gamma=0.5)

        # 
        self.max_mem = 50000
        self.batch = 1000
        self.learning_rate = 0.001
        self.game = Game(1600, 900)


        self.memory_queue = deque(maxlen=self.max_mem)

    def get_surrounding_points(self, current_pos, current_dir):
        left_point = current_pos + Direction.get_counterclockwise(current_dir)
        straight_point = current_pos + current_dir
        right_point = current_dir + Direction.get_clockwise(current_dir)
        return [left_point, straight_point, right_point]
    

    def get_surrounding_danger(self, player, points):
        left, straight, right = points
        left_danger = player.is_next_point_possible(left)
        straight_danger = player.is_next_point_possible(straight)
        right_danger = player.is_next_point_possible(right)
        return [left_danger, straight_danger, right_danger]


    def get_current_state(self, game):
        game = Game(100, 100)
        player = game.player
        fruit = game.fruit

        points = self.get_surrounding_points(player.get_current_head_pos(), player.get_current_direction())
        left_danger, straight_danger, right_danger = self.get_surrounding_danger(player, points)        
        
        return [
            left_danger,
            straight_danger,
            right_danger
            
        ]


    def remember(self, state, action, reward, next_state, game_over):
        pass

    def train_on_long_memory(self):
        pass

    def train_on_short_memory(self,  state, action, reward, next_state, game_over):
        pass

    def get_action(self, state):
        pass


