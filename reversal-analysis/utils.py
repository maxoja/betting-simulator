import matplotlib.pyplot as plt

def plot_histogram_unblock(sample_data):
    plt.figure()
    plt.hist(sample_data, bins=128)
    plt.show(block=False)

def plot_centered_cumulative_histogram(sample_data, center_val=0):
    if not sample_data:
        plt.figure()
        plt.plot([])
        plt.show(block=False)
        return
    sample_data = sorted(sample_data)
    mean_index = min(range(len(sample_data)), key=lambda i: abs(center_val-sample_data[i]))
    count_y = [abs(mean_index-i)/len(sample_data)*100 for i,val in enumerate(sample_data)]
    count_x = sample_data[::]
    plt.figure()
    plt.plot(count_x, count_y)
    plt.show(block=False)

def show_plot():
    plt.show()

def avg(l):
    return sum(l)/len(l)