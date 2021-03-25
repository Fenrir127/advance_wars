import pickle
import numpy as np
import copy
import matplotlib.pyplot as plt
from matplotlib import style
from setting import GRID_X_SIZE, GRID_Y_SIZE, MAP_TO_LOAD, LEARNING_SK1, Q_TABLE_NAME_SK1, STARTING_TABLE, ITERATIVE_TRAINING
from os import path

style.use("ggplot")

LEARNING_RATE = 0.3
DISCOUNT = 0.95
AVG_EVERY = 20
SCN_SHOW_EVERY = 1000

SHOW_EVERY = 10000

episode_rewards = []
iteration = 0

MAP_SIZE = (7, 7)
UNIT_SPEED = 3
UNIT_RANGE = 1
UNIT_MAX_RANGE = UNIT_RANGE + UNIT_SPEED
DISCRETE_ENV_SIZE = [7, 7, 7, 7]  # skynet pos x, skynet pos y, en pos x, en pos y
ACTION_TABLE = [
    [(-3, 0), (0, 0)],
    [(-3, 0), (1, 0)],
    [(-3, 0), (0, 1)],
    [(-3, 0), (-1, 0)],
    [(-3, 0), (0, -1)],

    [(-2, -1), (0, 0)],
    [(-2, -1), (1, 0)],
    [(-2, -1), (0, 1)],
    [(-2, -1), (-1, 0)],
    [(-2, -1), (0, -1)],

    [(-2, 0), (0, 0)],
    [(-2, 0), (1, 0)],
    [(-2, 0), (0, 1)],
    [(-2, 0), (-1, 0)],
    [(-2, 0), (0, -1)],

    [(-2, 1), (0, 0)],
    [(-2, 1), (1, 0)],
    [(-2, 1), (0, 1)],
    [(-2, 1), (-1, 0)],
    [(-2, 1), (0, -1)],

    [(-1, -2), (0, 0)],
    [(-1, -2), (1, 0)],
    [(-1, -2), (0, 1)],
    [(-1, -2), (-1, 0)],
    [(-1, -2), (0, -1)],

    [(-1, -1), (0, 0)],
    [(-1, -1), (1, 0)],
    [(-1, -1), (0, 1)],
    [(-1, -1), (-1, 0)],
    [(-1, -1), (0, -1)],

    [(-1, 0), (0, 0)],
    [(-1, 0), (1, 0)],
    [(-1, 0), (0, 1)],
    [(-1, 0), (-1, 0)],
    [(-1, 0), (0, -1)],

    [(-1, 1), (0, 0)],
    [(-1, 1), (1, 0)],
    [(-1, 1), (0, 1)],
    [(-1, 1), (-1, 0)],
    [(-1, 1), (0, -1)],

    [(-1, 2), (0, 0)],
    [(-1, 2), (1, 0)],
    [(-1, 2), (0, 1)],
    [(-1, 2), (-1, 0)],
    [(-1, 2), (0, -1)],

    [(0, -3), (0, 0)],
    [(0, -3), (1, 0)],
    [(0, -3), (0, 1)],
    [(0, -3), (-1, 0)],
    [(0, -3), (0, -1)],

    [(0, -2), (0, 0)],
    [(0, -2), (1, 0)],
    [(0, -2), (0, 1)],
    [(0, -2), (-1, 0)],
    [(0, -2), (0, -1)],

    [(0, -1), (0, 0)],
    [(0, -1), (1, 0)],
    [(0, -1), (0, 1)],
    [(0, -1), (-1, 0)],
    [(0, -1), (0, -1)],

    [(0, 0), (0, 0)],
    [(0, 0), (1, 0)],
    [(0, 0), (0, 1)],
    [(0, 0), (-1, 0)],
    [(0, 0), (0, -1)],

    [(0, 1), (0, 0)],
    [(0, 1), (1, 0)],
    [(0, 1), (0, 1)],
    [(0, 1), (-1, 0)],
    [(0, 1), (0, -1)],

    [(0, 2), (0, 0)],
    [(0, 2), (1, 0)],
    [(0, 2), (0, 1)],
    [(0, 2), (-1, 0)],
    [(0, 2), (0, -1)],

    [(0, 3), (0, 0)],
    [(0, 3), (1, 0)],
    [(0, 3), (0, 1)],
    [(0, 3), (-1, 0)],
    [(0, 3), (0, -1)],

    [(1, -2), (0, 0)],
    [(1, -2), (1, 0)],
    [(1, -2), (0, 1)],
    [(1, -2), (-1, 0)],
    [(1, -2), (0, -1)],

    [(1, -1), (0, 0)],
    [(1, -1), (1, 0)],
    [(1, -1), (0, 1)],
    [(1, -1), (-1, 0)],
    [(1, -1), (0, -1)],

    [(1, 0), (0, 0)],
    [(1, 0), (1, 0)],
    [(1, 0), (0, 1)],
    [(1, 0), (-1, 0)],
    [(1, 0), (0, -1)],

    [(1, 1), (0, 0)],
    [(1, 1), (1, 0)],
    [(1, 1), (0, 1)],
    [(1, 1), (-1, 0)],
    [(1, 1), (0, -1)],

    [(1, 2), (0, 0)],
    [(1, 2), (1, 0)],
    [(1, 2), (0, 1)],
    [(1, 2), (-1, 0)],
    [(1, 2), (0, -1)],

    [(2, -1), (0, 0)],
    [(2, -1), (1, 0)],
    [(2, -1), (0, 1)],
    [(2, -1), (-1, 0)],
    [(2, -1), (0, -1)],

    [(2, 0), (0, 0)],
    [(2, 0), (1, 0)],
    [(2, 0), (0, 1)],
    [(2, 0), (-1, 0)],
    [(2, 0), (0, -1)],

    [(2, 1), (0, 0)],
    [(2, 1), (1, 0)],
    [(2, 1), (0, 1)],
    [(2, 1), (-1, 0)],
    [(2, 1), (0, -1)],

    [(3, 0), (0, 0)],
    [(3, 0), (1, 0)],
    [(3, 0), (0, 1)],
    [(3, 0), (-1, 0)],
    [(3, 0), (0, -1)],

]
ACTION_POSSIBILITIES = len(ACTION_TABLE)  # for an infantry, it is 125 possible actions


def init_map():
    map_init = []
    # This opens the game map and reads the game tile (river, mountain, etc)
    # with open(path.join(path.dirname(__file__), 'MAP_TO_LOAD'), 'rt') as f1:
    if ITERATIVE_TRAINING:
        with open(path.join(path.dirname(__file__), 'scenario_stalemate.txt'), 'rt') as f1:
            for line in f1:
                map_init.append(line.strip())
    else:
        with open(path.join(path.dirname(__file__), MAP_TO_LOAD), 'rt') as f1:
            for line in f1:
                map_init.append(line.strip())

    converter = {'w': 1, 'r': 2, 'p': 1, 'm': 2, 'd': 1, 's': 10}
    mvt_cost_map = [[0 for x in range(GRID_X_SIZE)] for y in range(GRID_Y_SIZE)]
    # This converts every tile to a mvmt cost
    for x in range(GRID_X_SIZE):
        for y in range(GRID_Y_SIZE):
            mvt_cost_map[y][x] = converter[map_init[y][x]]
    return mvt_cost_map


def graph():
    moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,)) / SHOW_EVERY, mode='valid')
    plt.plot([i for i in range(len(moving_avg))], moving_avg)
    plt.ylabel(f"Reward {SHOW_EVERY}ma")
    plt.xlabel("iteration #")
    plt.show(block=False)
    plt.pause(0.1)


def graph_by_scenario():
    plt.clf()
    for index, scn_rewards in enumerate(Skynet.rewards):
        if scn_rewards:
            moving_avg = np.convolve(scn_rewards, np.ones((SCN_SHOW_EVERY,)) / SCN_SHOW_EVERY, mode='valid')
            plt.plot([i * AVG_EVERY for i in range(len(moving_avg))], moving_avg, label=f'Scenario {index}')
    plt.title(f"LR={LEARNING_RATE} ; D={DISCOUNT}")
    plt.ylabel(f"Reward {SCN_SHOW_EVERY}ma")
    plt.xlabel("iteration #")
    plt.legend(loc='best')
    plt.show(block=False)
    plt.pause(0.1)


def save_info(to_save, pickle_name):
    f = open(pickle_name, 'wb')
    f.write(pickle.dumps(to_save))
    f.close()


class Skynet:
    rewards = [[], [], []]
    rewards_tmp = [[], [], []]
    scenario_rewards = [[0, 0], [0, 0], [0, 0]]  # Win / lose
    version = 0

    def __init__(self, x, y, en_x, en_y, learning=LEARNING_SK1):
        self.learning = learning
        self.epsilon = 1
        self.iteration = 1
        self.action = 0
        self.skynet_mvt = 3  # Infantry
        self.skynet_range = 1  # Infantry
        self.skynet_pos_x = x
        self.skynet_pos_y = y
        self.en_pos_x = en_x
        self.en_pos_y = en_y

        self.q_table = np.zeros([1, 1, 1, 1] + [1])  # Just to initialize
        self.mvt_cost_map = init_map()
        self.legal_move = []  # This will be used during get_action, format: (mvt_x, mvt_y, atk_x, atk_y)

    def set_q_table(self, q_table):
        self.q_table = copy.copy(q_table)  # Copy by reference, in case of Skynet vs Skynet
        if not self.learning:
            self.epsilon = 0  # We want to exploit

    def get_action(self):
        self.legal_move = []  # Reset the table
        #  Get the new list of legal moves
        self.get_legal_move(self.skynet_mvt, self.skynet_pos_x, self.skynet_pos_y, self.en_pos_x, self.en_pos_y)
        if np.random.random() > self.epsilon:  # Maximum value
            self.action, _ = self.get_max_action(self.skynet_pos_x, self.skynet_pos_y, self.en_pos_x, self.en_pos_y)

        else:  # Random action
            # Gets a random legal move
            move = self.legal_move[np.random.randint(0, len(self.legal_move))]
            pos_x = move[0] - self.skynet_pos_x
            pos_y = move[1] - self.skynet_pos_y
            atk_x = move[2]
            atk_y = move[3]
            self.action = ACTION_TABLE.index([(pos_x, pos_y), (atk_x, atk_y)])
            # Get the action for the move, needed for get_reward
        return ACTION_TABLE[self.action]

    def get_reward(self, reward, new_skynet_x, new_skynet_y, en_new_x, en_new_y, scenario):
        self.legal_move = []  # Reset the table
        self.get_legal_move(self.skynet_mvt, new_skynet_x, new_skynet_y, en_new_x, en_new_y)  # We got
        _, max_future_q = self.get_max_action(new_skynet_x, new_skynet_y, en_new_x, en_new_y)
        # maximum possible value for the next state
        current_q = self.q_table[self.skynet_pos_x, self.skynet_pos_y, self.en_pos_x, self.en_pos_y, self.action]
        # current q_value that we need to modify because an action was taken
        new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
        # we find the new q_value of the current state and action according to the max possible value of the next state
        self.q_table[
            self.skynet_pos_x, self.skynet_pos_y, self.en_pos_x, self.en_pos_y, self.action] = new_q
        # we update the current q_table's q_value to represent the possibilities of this action

        self.set_param(new_skynet_x, new_skynet_y, en_new_x, en_new_y)
        self.interpret_reward(reward, scenario)

    def set_reward(self, reward, scenario):
        self.q_table[self.skynet_pos_x, self.skynet_pos_y, self.en_pos_x, self.en_pos_y, self.action] = reward
        self.interpret_reward(reward, scenario)

    def get_legal_move(self, mvt, x, y, enx, eny, direction="None"):
        if mvt < 0 or x < 0 or x > GRID_X_SIZE - 1 or y < 0 or y > GRID_Y_SIZE - 1:  # If tile is out of grid
            return
        if x == enx and y == eny:  # if on enemy tile
            return
        if abs(enx - x) + abs(eny - y) == self.skynet_range:  # enemy is one tile away
            if (x, y, enx - x, eny - y) not in self.legal_move:
                self.legal_move.append((x, y, enx - x, eny - y))
        if (x, y, 0, 0) not in self.legal_move:
            self.legal_move.append((x, y, 0, 0))

        if direction != "down":
            if y - 1 >= 0:
                mvt_cost = self.mvt_cost_map[y - 1][x]
                self.get_legal_move(mvt - mvt_cost, x, y - 1, enx, eny, "up")  # going up
        if direction != "right":
            if x - 1 >= 0:
                mvt_cost = self.mvt_cost_map[y][x - 1]
                self.get_legal_move(mvt - mvt_cost, x - 1, y, enx, eny, "left")  # going left
        if direction != "left":
            if x + 1 <= GRID_X_SIZE - 1:
                mvt_cost = self.mvt_cost_map[y][x + 1]
                self.get_legal_move(mvt - mvt_cost, x + 1, y, enx, eny, "right")  # going right
        if direction != "up":
            if y + 1 <= GRID_Y_SIZE - 1:
                mvt_cost = self.mvt_cost_map[y + 1][x]
                self.get_legal_move(mvt - mvt_cost, x, y + 1, enx, eny, "down")  # going down

    def set_param(self, x, y, en_x, en_y):
        self.skynet_pos_x = x
        self.skynet_pos_y = y
        self.en_pos_x = en_x
        self.en_pos_y = en_y

    def interpret_reward(self, reward, scenario):
        if self.learning:  # Need to show graph
            self.update_rewards(reward, scenario)
        else:
            if LEARNING_SK1 == 0:  # We are not learning anything, it's a SHOWDOWN
                self.iteration += 1
                if reward == 0:
                    Skynet.scenario_rewards[scenario][0] += 1
                elif reward == -2:
                    Skynet.scenario_rewards[scenario][1] += 1
                if self.iteration == 1000:
                    print(f"Result of Skynet with {STARTING_TABLE}")
                    print("---------------------------------------------------")
                    i = 0
                    for scenario in Skynet.scenario_rewards:
                        print(scenario)
                        print(f"SCENARIO {i}")
                        if scenario[1] == 0:
                            print("100%")
                        elif scenario[0] == 0:
                            print("0%")
                        else:
                            print(f'{100 * scenario[0] / (scenario[0] + scenario[1])}%')
                        i += 1
                    exit()

    def update_rewards(self, reward, scenario):
        episode_rewards.append(reward)
        if self.iteration % 1000 == 0:
            pass
            # print('\n' * 150)
            print("----------------------------")
            print(f'AI iterations: {self.iteration}')
            print(f'Epsilon: {self.epsilon}')
            print("----------------------------")
        if self.iteration % SHOW_EVERY == 0 and self.iteration != 0:
            graph_by_scenario()
        if self.iteration == 10 * SHOW_EVERY:
            self.epsilon = 0.75
            save_info(self.q_table, Q_TABLE_NAME_SK1)
            save_info(self.rewards, "new_rewards_stalemate.pickle")
        elif self.iteration == 20 * SHOW_EVERY:
            self.epsilon = 0.5
            save_info(self.q_table, Q_TABLE_NAME_SK1)
            save_info(self.rewards, "new_rewards_stalemate.pickle")
        elif self.iteration == 30 * SHOW_EVERY:
            self.epsilon = 0.25
            save_info(self.q_table, Q_TABLE_NAME_SK1)
            save_info(self.rewards, "new_rewards_stalemate.pickle")
        elif self.iteration == 40 * SHOW_EVERY:
            self.epsilon = 0
            save_info(self.q_table, Q_TABLE_NAME_SK1)
            save_info(self.rewards, "new_rewards_stalemate.pickle")
        elif self.iteration == 50 * SHOW_EVERY:
            save_info(self.q_table, Q_TABLE_NAME_SK1)
            save_info(self.rewards, "new_rewards_stalemate.pickle")
            print("Learning finished.")
            input("Press any key to exit.")
            exit()

        self.iteration += 1
        Skynet.rewards_tmp[scenario].append(reward)
        if len(Skynet.rewards_tmp[scenario]) == AVG_EVERY:
            Skynet.rewards[scenario].append(
                sum(Skynet.rewards_tmp[scenario]) / len(Skynet.rewards_tmp[scenario]))  # averages it to save memory
            Skynet.rewards_tmp[scenario] = []

    def get_max_action(self, x, y, en_x, en_y):  # Gets the best action considering the current parameters
        max_value = -999  # Will be overwritten
        max_action = -1  # Will be overwritten
        for move in self.legal_move:
            pos_x = move[0] - x
            pos_y = move[1] - y
            atk_x = move[2]
            atk_y = move[3]
            # Get the action for the move, then find its q value
            curr_action = ACTION_TABLE.index([(pos_x, pos_y), (atk_x, atk_y)])
            curr_value = self.q_table[x, y, en_x, en_y, curr_action]
            if curr_value > max_value:
                max_value = curr_value
                max_action = curr_action
        return max_action, max_value
