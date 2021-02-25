import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

style.use("ggplot")

LEARNING_RATE = 0.1
DISCOUNT = 0.95

SHOW_EVERY = 500
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
ACTION_POSSIBILITIES = len(ACTION_TABLE)  # for an infantry, it should be 125 possible actions

q_table = np.random.uniform(low=-2, high=0, size=(DISCRETE_ENV_SIZE + [ACTION_POSSIBILITIES]))

epsilon = 0.5
action = 0
skynet_pos_x = 0
skynet_pos_y = 3
en_pos_x = 6
en_pos_y = 3


def get_action(en_x, en_y):
    global action
    global skynet_pos_x
    global skynet_pos_y
    global en_pos_x
    global en_pos_y
    if np.random.random() > epsilon:
        action = np.argmax(q_table[skynet_pos_x, skynet_pos_y, en_x, en_y])
    else:
        action = np.random.randint(0, ACTION_POSSIBILITIES)
    to_do = ACTION_TABLE[action]
    return to_do


def get_reward(reward, new_skynet_x, new_skynet_y, en_new_x, en_new_y):
    global action
    global skynet_pos_x
    global skynet_pos_y
    global en_pos_x
    global en_pos_y
    max_future_q = np.max(q_table[new_skynet_x, new_skynet_y, en_new_x, en_new_y])
    # maximum possible value for the next situation
    current_q = q_table[skynet_pos_x, skynet_pos_y, en_pos_x, en_pos_y, action]
    # current state that we need to modify because an action was taken
    new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
    # we find the new q_value of the current state and action according to the max possible value of the next state
    q_table[skynet_pos_x, skynet_pos_y, en_pos_x, en_pos_y, action] = new_q
    skynet_pos_x = new_skynet_x
    skynet_pos_y = new_skynet_y
    en_pos_x = en_new_x
    en_pos_y = en_new_y
    # we update the current q_table's q_value to represent the possibilities of this action
    global iteration
    iteration += 1
    episode_rewards.append(reward) ####
    if iteration % SHOW_EVERY == 0:
        graph()


def reset():
    global epsilon
    global action
    global skynet_pos_x
    global skynet_pos_y
    global en_pos_x
    global en_pos_y
    epsilon = epsilon - 0.0001  # Will be 0 after 5000 resets
    skynet_pos_x = 0
    skynet_pos_y = 3
    en_pos_x = 6
    en_pos_y = 3


def graph():
    moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,)) / SHOW_EVERY, mode='valid')
    plt.plot([i for i in range(len(moving_avg))], moving_avg)
    plt.ylabel(f"Reward {SHOW_EVERY}ma")
    plt.xlabel("iteration #")
    plt.show(block=False)
    plt.pause(0.1)

def set_pos(x, y, en_x, en_y):
    global skynet_pos_x
    global skynet_pos_y
    global en_pos_x
    global en_pos_y

    skynet_pos_x = x
    skynet_pos_y = y
    en_pos_x = en_x
    en_pos_y = en_y