import pickle
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style


SCN_SHOW_EVERY = 1000
AVG_EVERY = 20
style.use("ggplot")


def graph(reward_file, learning_rate, discount):
    f = open(reward_file, 'rb')
    rewards = pickle.loads(f.read())
    plt.clf()
    for index, scn_rewards in enumerate(rewards):
        if scn_rewards:
            moving_avg = np.convolve(scn_rewards, np.ones((SCN_SHOW_EVERY,)) / SCN_SHOW_EVERY, mode='valid')
            plt.plot([i * AVG_EVERY for i in range(len(moving_avg))], moving_avg, label=f'Scenario {index}')
    plt.title(f"LR={learning_rate} ; D={discount}")
    plt.ylabel(f"Reward {SCN_SHOW_EVERY}ma")
    plt.xlabel("iteration #")
    plt.legend(loc='best')
    plt.show(block=False)
    plt.pause(0.1)


# graph('FINAL_rewards_stalemate_03.pickle', 0.3, 0.95)
# graph('FINAL_rewards_runaway.pickle', 0.3, 0.95)
# graph('FINAL_rewards_attack.pickle', 0.3, 0.95)
input("Press any key to exit.")