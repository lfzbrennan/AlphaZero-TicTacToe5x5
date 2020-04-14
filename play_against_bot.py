from game import Game, GameState
from base_model import Residual_CNN

import random
import config

from agent import Agent, User

def declare_winner(user_turn, value):
    if value == 0:
        print("Draw!!")
    if (value and user_turn) or (not value and not user_turn):
        print("You beat the bot!")
    else:
        print("The bot wins")

def get_user_action():
    return int(input("choose action"))
        
def print_board(state):
    board = state.get_board_render()
    columns = []
    for i in range(5):
        columns += [board[i*5:i*5+5]]
    for c in columns:
        print(c)

def play_game():
    user_turn = random.choice([True, False])
    env = Game()
    state = env.reset()

    bot_NN = Residual_CNN(config.REG_CONST, config.LEARNING_RATE, env.input_shape,   env.action_size, config.HIDDEN_CNN_LAYERS)
    bot_network = bot_NN.read()
    bot_NN.model.set_weights(bot_network.get_weights())

    bot = Agent('bot', env.state_size, env.action_size, config.MCTS_SIMS, config.CPUCT, bot_NN)

    board = state.get_number_render()
    columns = []
    for i in range(5):
        columns += [board[i*5:i*5+5]]
    for c in columns:
        print(c)

    while True:
        # print the board
        print_board(state)

        # get user/bots turn
        if not user_turn:
            action, _, _, _ = bot.act(state, 1)
        else:
            action = get_user_action()

        # bot chose action $ or you chose action $
        if user_turn: print(f"you chose action {action}")
        else: print(f"bot chose action {action}")

        state, value, done, _ = env.step(action)

        if done:
            declare_winner(user_turn, value)
            break
        
        user_turn = not user_turn;



def main():
    play_game()
    



if __name__ == "__main__":
    main()