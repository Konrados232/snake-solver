import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np


class Trainer:
    def __init__(self, model, learning_rate, gamma):
        self.model = model
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.optimizer = optim.Adam(model.parameters(), lr=self.learning_rate)        
        self.loss_func = nn.MSELoss()


    def _reshape(self, state, action, reward, next_state, game_over):
        state = torch.unsqueeze(state, 0)
        next_state = torch.unsqueeze(next_state, 0)
        action = torch.unsqueeze(action, 0)
        reward = torch.unsqueeze(reward, 0)
        game_over = (game_over, )

        return state, action, reward, next_state, game_over


    def _use_gpu(self, state, action, reward, next_state):
        state.cuda()
        next_state.cuda()
        action.cuda()
        reward.cuda()


    def train_step(self, state, action, reward, next_state, game_over):
        state = torch.tensor(np.array(state), dtype=torch.float)
        next_state = torch.tensor(np.array(next_state), dtype=torch.float)
        action = torch.tensor(np.array(action), dtype=torch.float)
        reward = torch.tensor(np.array(reward), dtype=torch.float)

        self._use_gpu(state, action, reward, next_state)

        if len(state.shape) == 1:
            state, action, reward, next_state, game_over = self._reshape(state, action, reward, next_state, game_over)
        
        # prediction of Q values in current state
        pred = self.model(state)

        target = pred.clone()

        for index, item in enumerate(game_over):
            Q_new = reward[index]
            if not game_over[index]:
                Q_new = reward[index] + self.gamma * torch.max(self.model(next_state[index]))

            target[index][torch.argmax(action).item()] = Q_new

        self.optimizer.zero_grad()
        loss = self.loss_func(target, pred)
        loss.backward()

        self.optimizer.step()
        