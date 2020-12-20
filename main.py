from random import random
from functools import reduce
import matplotlib.pyplot as plt
import config

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
    plt.hist(sample_data, bins=config.VISUAL_N_BINS)
    plt.show(block=False)

def plot_centered_cumulative_histogram(sample_data, center_val):
    sample_data = sorted(sample_data)
    mean_index = min(range(len(sample_data)), key=lambda i: abs(center_val-sample_data[i]))
    count_y = [abs(mean_index-i) for i,val in enumerate(sample_data)]
    count_x = sample_data[::]
    plt.figure()
    plt.plot(count_x, count_y)
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
    plot_centered_cumulative_histogram(final_balances, center_val=config.INITIAL_CAPITAL)
    plt.show()


