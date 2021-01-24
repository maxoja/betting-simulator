import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
import numpy as np

def plot_boxes(samples, labels, block=False):
    plt.figure()
    plt.boxplot(samples, labels=labels)
    plt.show(block=block)

def plot_lines(lines, title="", block=False):
    plt.figure()
    plt.title(title)
    for line in lines:
        plt.plot(line)
    plt.show(block=block)

def plot_histogram(sample_data, title="", color=None, block=False):
    plt.figure()
    plt.title(title)
    plt.hist(sample_data, color=color, bins=128)
    plt.show(block=block)

def plot_scatter(x, y, clr='blue', title="", block=False):
    plt.figure()
    plt.title(title)
    if not type(y) is tuple:
        y = [y]
    if not type(clr) is tuple:
        clr = [clr]
    for y_set, c in zip(y, clr):
        plt.scatter(x, y_set, c=c, s=2, alpha=0.5)
    plt.show(block=block)

def plot_dict_as_bars(d, title="", block=False):
    plt.figure()
    plt.title(title)
    plt.grid(axis='y')
    plt.bar(d.keys(), d.values())
    plt.xticks(rotation = 90)
    plt.tight_layout()
    plt.show(block=block)

def plot_outward_cumulative_hist(sample_data, center_val=0, title="", block=False):
    if not sample_data:
        plt.figure(title)
        plt.plot([])
        plt.show(block=block)
        return
    sample_data = sorted(sample_data)
    center_index = min(range(len(sample_data)), key=lambda i: abs(center_val-sample_data[i]))
    count_y = [abs(center_index-i)/len(sample_data)*100 for i,val in enumerate(sample_data)]
    count_x = sample_data[::]
    plt.figure(title)
    plt.plot(count_x, count_y)
    weights = np.ones_like(sample_data)/float(len(sample_data))*50
    plt.hist(sample_data, weights=weights, bins=128)
    plt.show(block=block)

def plot_cross_cumulative(data_a, data_b, title="", block=False):
    if len(data_a) == 0 and len(data_b) == 0:
        plt.figure()
        plt.title(title)
        plt.plot([])
        plt.show(block=block)
        return
        
    plt.figure()
    plt.title(title)
    
    data_a = sorted(data_a)
    # y_a = [i/len(data_a)*100 for i,val in enumerate(data_a)]
    y_a = [i for i,val in enumerate(data_a)]
    x_a = data_a[::]
    plt.plot(x_a, y_a)

    data_b = sorted(data_b)
    # y_b = [i/len(data_b)*100 for i,val in enumerate(data_b)]
    y_b = [i for i,val in enumerate(data_b)]
    x_b = data_b[::]
    plt.plot(x_b, y_b, color='red')

    min_x = int(min(min(x_a), min(x_b))) - 1
    max_x = int(max(max(x_a), max(x_b))) + 1
    range_x = range(min_x,max_x+1)
    y = []
    s = 0
    last_a = 0
    last_b = 0
    for x in range_x:
        while x_a and x_a[0] <= x:
            last_a = y_a[0]
            y_a.pop(0)
            x_a.pop(0)

        while x_b and x_b[0] <= x:
            last_b = y_b[0]
            y_b.pop(0)
            x_b.pop(0)

        s = last_a - last_b
        y.append(s)
    
    plt.plot(range_x, y, color='pink')
    plt.show(block=block)


def plot_for_stoploss(sample_data, profits, center_val=0, title="", block=False):
    if not sample_data:
        plt.figure()
        plt.title(title)
        plt.plot([])
        plt.show(block=block)
        return

    _, axs = plt.subplots(3,1, sharex=True)
    ax1 = axs[0]
    ax2 = axs[1]
    ax3 = axs[2]

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
    ax1.set_title(title)
    BLUE = 'C0'
    ORANGE = 'C1'
    RED = 'C3'
    GREEN = 'C2'
    BLACK = "#000000"
    
    # [OK]
    ax1.plot(count_x, norm_acc_pf_y, GREEN, label="cumu prof at normal exit without SL (<<)") # cumulative profit if trades from the right exit at the end of holding period
    # []
    ax1.plot(count_x, norm_acc_dd_y, RED, label='cumu loss at DD (>>)') # cumulative loss if trades from the left exit at dd
    # []
    # cumulative loss if trades from the left exit at stoploss of X value
    acc_qq_y = np.array([(i+1)*-sample_data[i] for i,acc_dd in enumerate(norm_acc_dd_y)])
    norm_acc_qq_y = acc_qq_y / max(max(acc_qq_y), abs(min(acc_qq_y)))*100
    ax1.plot(count_x, norm_acc_qq_y, ORANGE, label='cumu loss at SL set at DD (>>)')

    # [OK]
    ax1.plot(count_x, count_y, BLUE, label='cumulative trade dist by DD (<<)') # cumulative distribution of trades over worst dd

    # [OK]
    weights = np.ones_like(sample_data)/float(len(sample_data))*50
    ax1.hist(sample_data, color=BLUE, weights=weights, bins=128, label='trade dist by DD') # trades distributed by worst dd

    ax1.legend(fontsize="x-small")

    ax2.plot(count_x, acc_pf_y, GREEN, label="cumu prof at normal exit without SL (<<)")
    ax2.plot(count_x, acc_qq_y, ORANGE, label='cumu loss at SL set at DD (>>)')
    net = acc_pf_y - acc_qq_y
    ax2.plot(count_x, net, BLACK, linewidth=1.5, label='net')
    # plt.plot(count_x, net/acc_qq_y/100, GREY, linewidth=1.5, label='recovery factor')
    # [OK]
    weights = np.ones_like(sample_data)/float(len(sample_data))*0.01
    ax2.hist(sample_data, color=BLUE, weights=weights, bins=128, label='trade dist by DD') # trades distributed by worst dd
    ax2.vlines(-0.0015, 0,max(acc_pf_y))
    ax2.legend(fontsize='x-small')

    recovery = net/acc_qq_y
    recovery = np.clip(recovery, -5, 5)
    ax3.plot(count_x, recovery)
    ax3.vlines(-0.00001*200, 0, max(recovery), color=BLACK)
    ax3.yaxis.set_major_locator(MultipleLocator(1))
    ax3.grid(True)
    plt.show(block=block) 

def block():
    plt.show()