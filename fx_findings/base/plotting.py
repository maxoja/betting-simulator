import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
import numpy as np
from ..base.enums import Direction, Clr

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

def plot_dict_as_line(d, title="", min_value=0, block=False):
    plt.figure()
    plt.title(title)
    plt.grid(axis='y')
    if type(d) is list:
        for i, _d in enumerate(d):
            plt.plot(list(_d.values()), label=str(i))
        d = d[0]
    else:
        plt.plot(list(d.values()))
    plt.legend()
    plt.xticks(range(len(d.values())), list(d.keys()), rotation=90)
    plt.ylim(bottom = min_value)
    plt.tight_layout()
    plt.show(block=block)

def plot_dicts_as_stacked_ribbons(d, title="", min_value=0, block=False):
    plt.figure()
    plt.title(title)
    plt.grid(axis='y')

    if not type(d) is list:
        d = [d]
        
    for i, _d in enumerate(d):
        line_25 = []
        line_50 = []
        line_75 = []

        for key, value in _d.items():
            sorted_val = sorted(value)
            size_val = len(value)
            i_25 = int((size_val-1)*0.4)
            i_50 = int((size_val-1)*0.5)
            i_75 = int((size_val-1)*0.6)
            v_25 = sorted_val[i_25]
            v_50 = sorted_val[i_50]
            v_75 = sorted_val[i_75]
            line_25.append(v_25)
            line_50.append(v_50)
            line_75.append(v_75)

        clr_mean = f'C{str(i+2)}'
        clr_fill = 'C1'
        label = str(i)
        # plt.plot(range(len(_d)), line_25, clr_mean, linewidth=0.15)
        plt.plot(range(len(_d)), line_50, clr_mean, label=label, linewidth=0.5)
        # plt.plot(range(len(_d)), line_75, clr_mean, linewidth=0.15)
        plt.fill_between(range(len(_d)), line_25, line_75, color=clr_fill,alpha = 0.1)
        
    d = d[0]
        
    plt.legend()
    plt.xticks(range(len(d.values())), list(d.keys()), rotation=90)
    plt.ylim(bottom = min_value)
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

# use case 1:   You know the RSI value at each trade and also the trade results.
#               The trades are categorised into 2 groups, gain and loss groups.
#               This plot visualises and help choosing which RSI thresholdis best
#               to exclude as many loss trades and remain as many gain trades.
def plot_threshold_cross_cumulation(prefer_group, unprefer_group, acc_dir:Direction=None, background='white', normalise=False, title="", block=False):
    if len(prefer_group) + len(unprefer_group) == 0:
        plt.figure()
        plt.title(title)
        plt.plot([])
        plt.show(block=block)
        return
        
    old_background = plt.rcParams['figure.facecolor']
    plt.rcParams['figure.facecolor'] = background

    if acc_dir == None:
        _, axs = plt.subplots(2,1, sharex=True)
        ax1 = axs[0]
        ax2 = axs[1]
    else:
        if acc_dir == Direction.LEFT:
            _, ax1 = plt.subplots(1,1)
        if acc_dir == Direction.RIGHT:
            _, ax2 = plt.subplots(1,1)
    
    len_prefer = len(prefer_group)
    len_unprefer = len(unprefer_group)
    prefer_group = sorted(prefer_group)
    unprefer_group = sorted(unprefer_group)

    x_a = prefer_group[::]
    x_b = unprefer_group[::]

    if normalise:
        y_a = list(np.arange(len_prefer)/len_prefer*100)
        y_b = list(np.arange(len_unprefer)/len_unprefer*100)
    else:
        y_a = list(range(len_prefer))
        y_b = list(range(len_unprefer))
    
    y_a_l = y_a[::-1]
    y_b_l = y_b[::-1]
    y_a_r = y_a[::]
    y_b_r = y_b[::]

    if acc_dir in [None, Direction.LEFT]:
        ax1.plot(x_a, y_a_l, color=Clr.DEFAULT_BLUE)
        ax1.plot(x_b, y_b_l, color=Clr.RED)

    if acc_dir in [None, Direction.RIGHT]:
        ax2.plot(x_a, y_a_r, color=Clr.DEFAULT_BLUE)
        ax2.plot(x_b, y_b_r, color=Clr.RED)
    
    min_x = int(min(x_a + x_b))
    max_x = int(max(x_a + x_b))
    range_x = range(min_x-1, max_x+1)
    y_l = []
    y_r = []
    net_l = 0
    net_r = 0
    last_a_l = 0
    last_a_r = 0
    last_b_l = 0
    last_b_r = 0

    for x in range_x:
        while x_a and x_a[0] <= x:
            last_a_r = y_a_r[0]
            last_a_l = y_a_l[0]
            y_a_r.pop(0)
            y_a_l.pop(0)
            x_a.pop(0)

        while x_b and x_b[0] <= x:
            last_b_r = y_b_r[0]
            last_b_l = y_b_l[0]
            y_b_r.pop(0)
            y_b_l.pop(0)
            x_b.pop(0)

        no_value = last_a_l == 0 or last_b_l == 0
        no_value_r = last_a_r == 0 or last_b_r == 0
        
        net_l = np.NaN if no_value else last_a_l - last_b_l
        net_r = np.NaN if no_value_r else last_a_r - last_b_r

        y_l.append(net_l)
        y_r.append(net_r)
    
    best_x_l = range_x[np.nanargmax(y_l)]
    best_y_l = np.nanmax(y_l)
    best_x_r = range_x[np.nanargmax(y_r)]
    best_y_r = np.nanmax(y_r)

    plt.suptitle(title)

    if acc_dir in [None, Direction.LEFT]:
        ax1.set_title(f'\n\nWHEN X > {best_x_l}, DELTA = {best_y_l}')
        ax1.hlines(0, min(range_x), max(range_x))
        ax1.plot(range_x, y_l, color=Clr.ROSE)
        ax1.vlines(best_x_l, -10, 10)

    if acc_dir in [None, Direction.RIGHT]:
        ax2.set_title(f'\n\nWHEN X < {best_x_r}, DELTA = {best_y_r}')
        ax2.hlines(0, min(range_x), max(range_x))
        ax2.plot(range_x, y_r, color=Clr.LAVENDER)
        ax2.vlines(best_x_r, -10, 10)
        
    plt.rcParams['figure.facecolor'] = old_background
    plt.tight_layout()
    plt.show(block=block)
    return best_y_l


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