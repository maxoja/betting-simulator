import matplotlib.pyplot as plt
import numpy as np

def plot_lines_unblock(lines, title=""):
    plt.figure()
    plt.title(title)
    for line in lines:
        plt.plot(line)
    plt.show(block=False)

def plot_histogram_unblock(sample_data, title=""):
    plt.figure(title)
    plt.hist(sample_data, bins=128)
    plt.show(block=False)


def plot_centered_cumulative_histogram(sample_data, center_val=0, title=""):
    if not sample_data:
        plt.figure(title)
        plt.plot([])
        plt.show(block=False)
        return
    sample_data = sorted(sample_data)
    center_index = min(range(len(sample_data)), key=lambda i: abs(center_val-sample_data[i]))
    count_y = [abs(center_index-i)/len(sample_data)*100 for i,val in enumerate(sample_data)]
    count_x = sample_data[::]
    plt.figure(title)
    plt.plot(count_x, count_y)
    weights = np.ones_like(sample_data)/float(len(sample_data))*50
    plt.hist(sample_data, weights=weights, bins=128)
    plt.show(block=False)


def plot_for_stoploss(sample_data, profits, center_val=0, title=""):
    if not sample_data:
        plt.figure(title)
        plt.plot([])
        plt.show(block=False)
        return
    profits = [x for _,x in sorted(zip(sample_data,profits))]
    sample_data = sorted(sample_data)
    center_index = min(range(len(sample_data))[::-1], key=lambda i: abs(center_val-sample_data[i]))
    count_y = [abs(center_index-i)/len(sample_data)*100 for i,val in enumerate(sample_data)]
    count_x = sample_data[::]
    acc_dd_y = np.cumsum(sample_data)*-100/abs(sum(sample_data))
    acc_pf_y = np.cumsum(profits[::-1])[::-1]
    acc_pf_y /= max(max(acc_pf_y), abs(min(acc_pf_y)))
    acc_pf_y *= 100
    # print(acc_pf_y)
    plt.figure()
    plt.title(title)
    plt.plot(count_x, count_y) # cumulative count of trades over drawdown size domains
    plt.plot(count_x, acc_dd_y) # cumulative value of drawdowns
    plt.plot(count_x, acc_pf_y) # cumulative profit of trades
    weights = np.ones_like(sample_data)/float(len(sample_data))*50
    plt.hist(sample_data, weights=weights, bins=128)
    # plt.hist(sample_data)
    plt.show(block=False)


def show_plot():
    plt.show()