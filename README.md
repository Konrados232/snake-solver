# Snake Solver
Machine Learning project focused on creating self playing Snake game that is trying to hit the highest score possible. Project can be divided into two parts - the first one is the Snake game itself, and the second one is reinforcement learning model.

## Game
Game itself is written in Python using Pygame library. The concept is simple - copied from the famous game Snake where moving part have to eat fruits in order to grow larger and score points. Snake itself is made with moving boxes in deque (for optimization) and able to move only in designated area.

## Reinforcement Learning
Learning part uses LinearQNet model from PyTorch library. It uses reward factor to learn to get better at the game where the reward is getting fruit correctly and it penalizes snake when it does nothing for long period of time or dies without getting any fruit.
