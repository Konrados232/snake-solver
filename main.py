from Game import Game
from Agent import Agent
from PlotHelp import plot
import pygame
import pygame_menu
import torch
import os.path

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = Game(width=1600, height=900)


    while True:
        old_state = agent.get_current_state(game)

        final_move = agent.get_action(old_state)

        reward, game_over, score = game.play_step(final_move)

        new_state = agent.get_current_state(game)

        agent.train_on_short_memory(old_state, final_move, reward, new_state, game_over)

        agent.remember(old_state, final_move, reward, new_state, game_over)

        if game_over:
            # train long memory
            game.reset()
            agent.rl_info.number_of_games += 1
            agent.train_on_long_memory()

            if score > record:
                record = score
                agent.model.save("./model", "model.pth")

            # print(f"Game {agent.rl_info.number_of_games}, Score")
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.rl_info.number_of_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


def model_without_training():
    agent = Agent()

    path = os.path.join("model","model.pth")
    if os.path.exists(path):
        agent.model.load_state_dict(torch.load(path))

    game = Game(width=1600, height=900)


    while True:
        old_state = agent.get_current_state(game)

        final_move = agent.get_action_without_training(old_state)

        reward, game_over, score = game.play_step(final_move)
        
        if game_over:
            # train long memory
            game.reset()


def play():
    Game(width=1600, height=900).main()

if __name__ == "__main__":
    pygame.init()
    
    surface = pygame.display.set_mode((600, 400))
    menu = pygame_menu.Menu('Welcome', 600, 400,
                       theme=pygame_menu.themes.THEME_BLUE)
    
    menu.add.button('Play', play)
    menu.add.button('Train model', train)
    menu.add.button('Use trained model', model_without_training)
    menu.mainloop(surface)