import numpy as np
import copy
import matplotlib.pyplot as plt
from matplotlib import style

style.use("ggplot")

LEARNING_RATE = 0.3
DISCOUNT = 0.95

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


class Skynet:

    def __init__(self, x, y, hp, en_x, en_y, en_hp):
        self.epsilon = 1
        self.action = 0
        self.skynet_pos_x = x
        self.skynet_pos_y = y
        self.skynet_hp = hp
        self.en_pos_x = en_x
        self.en_pos_y = en_y
        self.en_hp = en_hp
        self.iteration = 0
        self.q_table = np.random.uniform(low=-2, high=0, size=([1, 1, 1, 1, 1, 1] + [1]))  # WILL CHANGE

    def set_q_table(self, q_table):
        self.q_table = copy.copy(q_table)

    def get_action(self):
        if np.random.random() > self.epsilon:
            self.action = np.argmax(self.q_table[self.skynet_pos_x, self.skynet_pos_y, self.skynet_hp, self.en_pos_x,
                                                 self.en_pos_y, self.en_hp])
        else:
            self.action = np.random.randint(0, ACTION_POSSIBILITIES)
        return ACTION_TABLE[self.action]

    def get_reward(self, reward, new_skynet_x, new_skynet_y, new_skynet_hp, en_new_x, en_new_y, en_new_hp):
        max_future_q = np.max(self.q_table[new_skynet_x, new_skynet_y, new_skynet_hp, en_new_x, en_new_y, en_new_hp])
        # maximum possible value for the next situation
        current_q = self.q_table[self.skynet_pos_x, self.skynet_pos_y, self.skynet_hp, self.en_pos_x, self.en_pos_y,
                                 self.en_hp, self.action]
        # current state that we need to modify because an action was taken
        new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
        # we find the new q_value of the current state and action according to the max possible value of the next state
        self.q_table[self.skynet_pos_x, self.skynet_pos_y, self.skynet_hp, self.en_pos_x, self.en_pos_y, self.en_hp, self.action] = new_q
        self.skynet_pos_x = new_skynet_x
        self.skynet_pos_y = new_skynet_y
        self.skynet_hp = new_skynet_hp
        self.en_pos_x = en_new_x
        self.en_pos_y = en_new_y
        self.en_hp = en_new_hp

        # we update the current q_table's q_value to represent the possibilities of this action

        episode_rewards.append(reward)  ####
        if self.iteration % 1000 == 0:
            print(f'AI iterations: {self.iteration}')
            print(f'epsilon: {self.epsilon}')
        if self.iteration % SHOW_EVERY == 0 and self.iteration != 0:
            self.graph()

        if self.iteration == 100000:
            epsilon = 0.75
        elif self.iteration == 200000:
            epsilon = 0.5
        elif self.iteration == 300000:
            epsilon = 0.25
        elif self.iteration == 400000:
            epsilon = 0
        # epsilon = 1 - iteration/200000

        self.iteration += 1

    def graph(self):
        moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,)) / SHOW_EVERY, mode='valid')
        plt.plot([i for i in range(len(moving_avg))], moving_avg)
        plt.ylabel(f"Reward {SHOW_EVERY}ma")
        plt.xlabel("iteration #")
        plt.show(block=False)
        plt.pause(0.1)

    def set_param(self, x, y, hp, en_x, en_y, en_hp):
        self.skynet_pos_x = x
        self.skynet_pos_y = y
        self.skynet_hp = hp
        self.en_pos_x = en_x
        self.en_pos_y = en_y
        self.en_hp = en_hp
