import torch
import numpy as np
import random

from pygame import Vector2
from RLModelInfo import RLModelInfo
from Game import Game
from collections import deque
from Direction import Direction
from MLModel import Linear_QNet
from Trainer import Trainer


class Agent:
    def __init__(self):
        self.rl_info = RLModelInfo(number_of_games=0, epsilon=0, gamma=0.8)

        # 
        self.max_mem = 50000
        self.batch_size = 1000
        self.learning_rate = 0.001

        self.memory_queue = deque(maxlen=self.max_mem)

        self.model = Linear_QNet(11, 256, 3)
        self.trainer = Trainer(self.model, self.learning_rate, self.rl_info.gamma)


    def get_surrounding_points(self, current_pos, current_dir):
        counterclockwise = Direction.get_counterclockwise(current_dir).value
        left_point = current_pos + counterclockwise
        straight_point = current_pos + current_dir.value
        clockwise = Direction.get_clockwise(current_dir).value
        right_point = current_pos + clockwise
        return [left_point, straight_point, right_point]
    

    def get_surrounding_danger(self, game, points):
        left, straight, right = points
        left_danger = game.is_next_point_possible(left)
        straight_danger = game.is_next_point_possible(straight)
        right_danger = game.is_next_point_possible(right)
        return [left_danger, straight_danger, right_danger]


    def get_current_state(self, game):
        player = game.player
        fruit = game.fruit

        points = self.get_surrounding_points(player.get_current_head_pos(), player.get_current_direction())
        left_danger, straight_danger, right_danger = self.get_surrounding_danger(game, points)        
        
        moving_left = player.current_direction == Direction.LEFT
        moving_right = player.current_direction == Direction.RIGHT
        moving_up = player.current_direction == Direction.UP
        moving_down = player.current_direction == Direction.DOWN

        fruit_left = fruit.get_fruit_pos().x < player.get_current_head_pos().x
        fruit_right = fruit.get_fruit_pos().x > player.get_current_head_pos().x
        fruit_up =  fruit.get_fruit_pos().y < player.get_current_head_pos().y
        fruit_down = fruit.get_fruit_pos().y > player.get_current_head_pos().y


        state = [
            left_danger,
            straight_danger,
            right_danger,

            moving_left,
            moving_right,
            moving_up,
            moving_down,

            fruit_left,
            fruit_right,
            fruit_up,
            fruit_down
        ]

        return np.array(state, dtype=int)


    def remember(self, state, action, reward, next_state, game_over):
        self.memory_queue.append((state, action, reward, next_state, game_over))


    def train_on_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)


    def train_on_long_memory(self):
        if len(self.memory_queue) > self.batch_size:
            min_sample = random.sample(self.memory_queue, self.batch_size)
        else:
            min_sample = self.memory_queue


        state, action, reward, next_state, game_over = zip(*min_sample)
        self.trainer.train_step(state, action, reward, next_state, game_over)
        #for state, action, reward, next_state, game_over in min_sample:


    def get_action(self, state):
        self.rl_info.epsilon = 80 - self.rl_info.number_of_games

        final_move = [0,0,0]

        if random.randint(0, 200) < self.rl_info.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

