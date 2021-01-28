import numpy as np

LEARNING_RATE = 0.1
DISCOUNT = 0.95
EPISODES = 25000

MAP_SIZE = (5, 5)
UNIT_SPEED = 3
MVMT_POSSIBILITIES = 25
DISCRETE_OS_SIZE = [MAP_SIZE[0], MAP_SIZE[1]]
MVMT_TABLE = [(0, 0), (0, 1), (1, 0), (0, -1), (-1, 0),
              (0, 2), (0, -2), (1, 1), (-1, 1), (1, -1), (-1, -1), (2, 0), (-2, 0),
              (0, 3), (0, -3), (1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1),
              (2, -1), (-2, -1), (3, 0), (-3, 0)]

q_table = np.random.uniform(low=-8, high=0, size=(DISCRETE_OS_SIZE + [MVMT_POSSIBILITIES]))
epsilon = 0.5

def get_action(pos_x, pos_y, delta_x, delta_y):
    # return x, y
    legal_move = False
    while not legal_move:
        if np.random.random() > epsilon:
            action = np.argmax(q_table[delta_x, delta_y])
        else:
            action = np.random.randint(0, MVMT_POSSIBILITIES)
        mvmt = MVMT_TABLE[action]
        if pos_x + mvmt[0] >= MAP_SIZE[0] or pos_x + mvmt[0] < 0 or pos_y + mvmt[1] >= MAP_SIZE[1] or pos_y + mvmt[
            1] < 0:
            pass
            # print("Illegal move, looking for another one.")
        else:
            # print(f"Legal move. Sending {mvmt[0]} and {mvmt[1]} to the game.")
            legal_move = True
            return mvmt[0], mvmt[1], action


def get_reward(reward, action, current_delta_x, current_delta_y, new_delta_x, new_delta_y):
    max_future_q = np.max(q_table[new_delta_x, new_delta_y])
    current_q = q_table[current_delta_x, current_delta_y, action]
    new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
    q_table[current_delta_x, current_delta_y, action] = new_q


def reset():
    current_delta_x = 0
    current_delta_y = 0
    action = 0

# done = False

# while not done:
# 	action = np.argmax(q_table[discrete_state])
# 	new_state, reward, done, _ = env.step(action)
# 	new_discrete_state = get_discrete_state(new_state)
# 	env.render()
# 	if not done:
# 		max_future_q = np.max(q_table[new_discrete_state])
# 		current_q = q_table[discrete_state + (action, ) ]
