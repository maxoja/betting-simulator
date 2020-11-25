import matplotlib.pyplot as plt
import config
from random import random

def bet(odds):
    return odds >= random()

def plot_lines_unblock(list_of_lines, h_lines=[]):
    plt.figure()
    for line in list_of_lines:
        plt.plot(line)
    for h_val in h_lines:
        plt.hlines(h_val, 0, config.N_BETS)
    plt.show(block=False)

def plot_histogram_unblock(sample_data):
    plt.figure()
    plt.hist(sample_data, bins=256)
    plt.show(block=False)

if __name__ == '__main__':
    simulation_results = []

    for sim_id in range(config.N_SIMULATIONS):
        growth_points = [config.INITIAL_CAPITAL,]

        for i in range(config.N_BETS):
            current_capital = growth_points[-1]
            bet_size = current_capital * config.BET_SIZE_RATIO
            current_capital -= bet_size
            win_bet = bet(config.ODDS)
            if win_bet:
                current_capital += bet_size*2
            growth_points.append(current_capital)
        simulation_results.append(growth_points)

    final_balances = [result[-1] for result in simulation_results]
    print('init', config.INITIAL_CAPITAL*config.N_SIMULATIONS)
    print('total', sum(final_balances))

    plot_lines_unblock(simulation_results, config.THRESHOLDS)
    plot_histogram_unblock(final_balances)
    plt.show()


