import numpy as np
import copy
import matplotlib.pyplot as plt
from matplotlib import style
from setting import GRID_X_SIZE, GRID_Y_SIZE, MAP_TO_LOAD
from os import path

style.use("ggplot")

LEARNING_RATE = 0.3
DISCOUNT = 0.95
AVG_EVERY = 20
SCN_SHOW_EVERY = 1000

SHOW_EVERY = 100000

episode_rewards = []
iteration = 0

MAP_SIZE = (7, 7)
UNIT_SPEED = 3
UNIT_RANGE = 1
UNIT_MAX_RANGE = UNIT_RANGE + UNIT_SPEED
DISCRETE_ENV_SIZE = [7, 7, 2, 7, 7, 2]  # skynet pos x, skynet pos y, skynet hp range, en pos x, en pos y, en hp range
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
    with open(path.join(path.dirname(__file__), MAP_TO_LOAD), 'rt') as f1:
        for line in f1:
            map_init.append(line.strip())

    converter = {'w': 1, 'r': 2, 'p': 1, 'm': 2, 'd': 1}
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


class Skynet:

    def __init__(self, x, y, hp, en_x, en_y, en_hp):
        self.rewards = [[], [], []]
        self.rewards_tmp = [[], [], []]
        self.epsilon = 1
        self.action = 0
        self.skynet_mvt = 3  # Infantry
        self.skynet_range = 1  # Infantry
        self.skynet_pos_x = x
        self.skynet_pos_y = y
        self.skynet_hp = hp
        self.en_pos_x = en_x
        self.en_pos_y = en_y
        self.en_hp = en_hp
        self.iteration = 0
        self.q_table = np.random.uniform(low=-1, high=1, size=([1, 1, 1, 1, 1, 1] + [1]))  # Just to initialize
        self.mvt_cost_map = init_map()
        self.legal_move = []  # This will be used during get_action, format: (mvt_x, mvt_y, atk_x, atk_y)

    def set_q_table(self, q_table):
        self.q_table = copy.copy(q_table)  # Copy by reference

    def get_action(self):
        self.legal_move = []  # Reset the table
        #  Get the new list of legal moves
        self.get_legal_move(self.skynet_mvt, self.skynet_pos_x, self.skynet_pos_y, self.en_pos_x, self.en_pos_y)

        if np.random.random() > self.epsilon:  # Maximum value
            max_value = -2   # Will be overwritten
            max_action = -1  # Will be overwritten
            for move in self.legal_move:
                pos_x, pos_y, atk_x, atk_y = move
                # Get the action for the move, then find its q value
                curr_action = ACTION_TABLE.index([(pos_x, pos_y), (atk_x, atk_y)])
                curr_value = self.q_table[self.skynet_pos_x, self.skynet_pos_y, self.skynet_hp, self.en_pos_x,
                                          self.en_pos_y, self.en_hp, curr_action]
                if curr_value > max_value:
                    max_value = curr_value
                    max_action = curr_action
            self.action = max_action

        else:  # Random action
            # Gets a random legal move
            pos_x, pos_y, atk_x, atk_y = self.legal_move[np.random.randint(0, len(self.legal_move))]
            self.action = ACTION_TABLE.index([(pos_x, pos_y), (atk_x, atk_y)])
            # Get the action for the move, needed for get_reward
        return ACTION_TABLE[self.action]

    def get_reward(self, reward, new_skynet_x, new_skynet_y, new_skynet_hp, en_new_x, en_new_y, en_new_hp, scenario):
        self.update_rewards(reward, scenario)
        max_future_q = np.max(self.q_table[new_skynet_x, new_skynet_y, new_skynet_hp, en_new_x, en_new_y, en_new_hp])
        # maximum possible value for the next situation
        current_q = self.q_table[self.skynet_pos_x, self.skynet_pos_y, self.skynet_hp, self.en_pos_x, self.en_pos_y,
                                 self.en_hp, self.action]
        # current state that we need to modify because an action was taken
        new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
        # we find the new q_value of the current state and action according to the max possible value of the next state
        self.q_table[
            self.skynet_pos_x, self.skynet_pos_y, self.skynet_hp, self.en_pos_x, self.en_pos_y, self.en_hp, self.action] = new_q
        self.skynet_pos_x = new_skynet_x
        self.skynet_pos_y = new_skynet_y
        self.skynet_hp = new_skynet_hp
        self.en_pos_x = en_new_x
        self.en_pos_y = en_new_y
        self.en_hp = en_new_hp

        # we update the current q_table's q_value to represent the possibilities of this action

        episode_rewards.append(reward)
        if self.iteration % 1000 == 0:
            print(f'AI iterations: {self.iteration}')
            print(f'epsilon: {self.epsilon}')
        if self.iteration % SHOW_EVERY == 0 and self.iteration != 0:
            self.graph_by_scenario()
        if self.iteration == 100000:
            self.epsilon = 0.75
        elif self.iteration == 200000:
            self.epsilon = 0.5
        elif self.iteration == 300000:
            self.epsilon = 0.25
        elif self.iteration == 400000:
            self.epsilon = 0

        self.iteration += 1

    def get_legal_move(self, mvt, x, y, enx, eny, direction="None"):
        if mvt < 0 or x < 0 or x > GRID_X_SIZE - 1 or y < 0 or y > GRID_Y_SIZE - 1:  # If tile is out of grid
            return
        if x == enx and y == eny:  # if on enemy tile
            return
        if abs(enx - x) + abs(eny - y) == self.skynet_range:  # enemy is one tile away
            if (x - self.skynet_pos_x, y - self.skynet_pos_y, enx-x, eny-y) not in self.legal_move:
                self.legal_move.append((x - self.skynet_pos_x, y - self.skynet_pos_y, enx-x, eny-y))
        if (x - self.skynet_pos_x, y - self.skynet_pos_y, 0, 0) not in self.legal_move:
            self.legal_move.append((x - self.skynet_pos_x, y - self.skynet_pos_y, 0, 0))

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

    def set_param(self, x, y, hp, en_x, en_y, en_hp):
        self.skynet_pos_x = x
        self.skynet_pos_y = y
        self.skynet_hp = hp
        self.en_pos_x = en_x
        self.en_pos_y = en_y
        self.en_hp = en_hp

    def update_rewards(self, reward, scenario):
        self.rewards_tmp[scenario].append(reward)
        if len(self.rewards_tmp[scenario]) == AVG_EVERY:
            self.rewards[scenario].append(
                sum(self.rewards_tmp[scenario]) / len(self.rewards_tmp[scenario]))  # averages it to save memory
            self.rewards_tmp[scenario] = []

    def graph_by_scenario(self):
        plt.clf()
        for index, scn_rewards in enumerate(self.rewards):
            moving_avg = np.convolve(scn_rewards, np.ones((SCN_SHOW_EVERY, )) / SCN_SHOW_EVERY, mode = 'valid')
            plt.plot([i * AVG_EVERY for i in range(len(moving_avg))], moving_avg, label=f'Scenario {index}')
        plt.title(f"LR={LEARNING_RATE} ; D={DISCOUNT}")
        plt.ylabel(f"Reward {SCN_SHOW_EVERY}ma")
        plt.xlabel("iteration #")
        plt.legend(loc='best')
        plt.show(block=False)
        plt.pause(0.1)