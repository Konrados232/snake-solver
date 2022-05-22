from Game import Game
from Agent import Agent
from PlotHelp import plot


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





if __name__ == "__main__":
    train()