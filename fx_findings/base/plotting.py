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
    acc_dd_y = np.cumsum(sample_data)
    norm_acc_dd_y = acc_dd_y/abs(sum(sample_data))*-100
    acc_pf_y = np.cumsum(profits[::-1])[::-1]
    norm_acc_pf_y = acc_pf_y / max(max(acc_pf_y), abs(min(acc_pf_y))) * 100
    # print(acc_pf_y)
    plt.figure()
    plt.title(title)
    BLUE = 'C0'
    ORANGE = 'C1'
    RED = 'C3'
    GREEN = 'C2'
    TEAL = '#17becf'
    BLACK = "#000000"
    GREY = "#999999"
    
    # [OK]
    plt.plot(count_x, norm_acc_pf_y, GREEN, label="cumu prof at normal exit without SL (<<)") # cumulative profit if trades from the right exit at the end of holding period
    # []
    plt.plot(count_x, norm_acc_dd_y, RED, label='cumu loss at DD (>>)') # cumulative loss if trades from the left exit at dd
    # []
    # cumulative loss if trades from the left exit at stoploss of X value
    acc_qq_y = np.array([(i+1)*-sample_data[i] for i,acc_dd in enumerate(norm_acc_dd_y)])
    norm_acc_qq_y = acc_qq_y / max(max(acc_qq_y), abs(min(acc_qq_y)))*100
    plt.plot(count_x, norm_acc_qq_y, ORANGE, label='cumu loss at SL set at DD (>>)')

    # [OK]
    plt.plot(count_x, count_y, BLUE, label='cumulative trade dist by DD (<<)') # cumulative distribution of trades over worst dd

    # [OK]
    weights = np.ones_like(sample_data)/float(len(sample_data))*50
    plt.hist(sample_data, color=BLUE, weights=weights, bins=128, label='trade dist by DD') # trades distributed by worst dd

    plt.legend(fontsize="x-small")

    plt.figure()
    plt.plot(count_x, acc_pf_y, GREEN, label="cumu prof at normal exit without SL (<<)")
    plt.plot(count_x, acc_qq_y, ORANGE, label='cumu loss at SL set at DD (>>)')
    net = acc_pf_y - acc_qq_y
    plt.plot(count_x, net, BLACK, linewidth=1.5, label='net')
    # plt.plot(count_x, net/acc_qq_y/100, GREY, linewidth=1.5, label='recovery factor')
    # [OK]
    weights = np.ones_like(sample_data)/float(len(sample_data))*0.01
    plt.hist(sample_data, color=BLUE, weights=weights, bins=128, label='trade dist by DD') # trades distributed by worst dd
    plt.legend(fontsize='x-small')

    plt.show(block=False) 


def show_plot():
    plt.show()