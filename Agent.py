import torch
import numpy as np
import random

from RLModelInfo import RLModelInfo
from collections import deque
from Direction import Direction
from MLModel import Linear_QNet
from Trainer import Trainer


class Agent:
    def __init__(self):
        self.rl_info = RLModelInfo(number_of_games=0, epsilon=0, gamma=0.9, learning_rate=0.001,
                            input_vector_size=11, output_vector_size=3, number_of_layers=1, layer_sizes=[256], 
                            maximum_memory=50000, batch_size=1000, number_of_games_for_training=180, random_scale=200)

        self.memory_queue = deque(maxlen=self.rl_info.maximum_memory)

        self.model = Linear_QNet(self.rl_info.input_vector_size, self.rl_info.number_of_layers, self.rl_info.layer_sizes, self.rl_info.output_vector_size)
        self.trainer = Trainer(self.model, self.rl_info.learning_rate, self.rl_info.gamma)


    def _get_surrounding_points(self, current_pos, current_dir):
        counterclockwise = Direction.get_counterclockwise(current_dir).value
        left_point = current_pos + counterclockwise
        straight_point = current_pos + current_dir.value
        clockwise = Direction.get_clockwise(current_dir).value
        right_point = current_pos + clockwise
        return [left_point, straight_point, right_point]
    

    def _get_surrounding_danger(self, game, points):
        left, straight, right = points
        left_danger = game.is_next_point_possible(left)
        straight_danger = game.is_next_point_possible(straight)
        right_danger = game.is_next_point_possible(right)
        return [left_danger, straight_danger, right_danger]


    def get_current_state(self, game):
        player = game.player
        fruit = game.fruit

        points = self._get_surrounding_points(player.get_current_head_pos(), player.get_current_direction())
        left_danger, straight_danger, right_danger = self._get_surrounding_danger(game, points)        
        
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
        if len(self.memory_queue) > self.rl_info.batch_size:
            min_sample = random.sample(self.memory_queue, self.rl_info.batch_size)
        else:
            min_sample = self.memory_queue


        state, action, reward, next_state, game_over = zip(*min_sample)
        self.trainer.train_step(state, action, reward, next_state, game_over)
        #for state, action, reward, next_state, game_over in min_sample:


    def get_action(self, state):
        self.rl_info.epsilon = self.rl_info.number_of_games_for_training - self.rl_info.number_of_games

        final_move = [0,0,0]

        if random.randint(0, self.rl_info.random_scale) < self.rl_info.epsilon:
            move = random.randint(0, len(final_move) - 1)
            final_move[move] = 1
            return final_move
        else:
            return self.get_action_without_training(state)


    def get_action_without_training(self, state):
        final_move = [0,0,0]

        state0 = torch.tensor(state, dtype=torch.float)
        prediction = self.model(state0)
        move = torch.argmax(prediction).item()
        final_move[move] = 1

        return final_move