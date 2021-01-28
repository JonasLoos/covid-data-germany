import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os



def average(data):
	'''7d moving average (3 back, 3 forward in time)'''
	result = np.zeros(data.shape[0]-3)
	data = np.append(np.zeros(3), data, axis=0)
	for i in range(7):
		result += data[i:data.shape[0]-6+i]
	result /= 7
	return result


def plot():
    fig, ax1 = plt.subplots(1, figsize=(12,8))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.'))
    ax1.set_xlabel('date')
    ax1.set_ylim(0,40000)
    # ax1.xaxis.set_major_locator(mdates.DayLocator(interval=n//10))
    ax2 = ax1.twinx()
    ax2.set_ylim(0,2000)

    for x, ax, color in [('cases', ax1, 'blue'), ('deaths', ax2, 'red')]:
        yesterday, today = [np.genfromtxt(f'{x}/{day}', delimiter=',') for day in sorted(os.listdir(x))[-2:]]
        n = today.shape[1]
        ax.plot(today[1:,1:].sum(axis=0), color=color, linestyle='dotted')
        ax.plot(average(today[1:,1:].sum(axis=0)), color=color)
        ax.tick_params(axis='y', labelcolor=color)
        ax.set_ylabel(x, color=color)

    fig.tight_layout()
    plt.savefig('plots/new_data.png', dpi=300)


if __name__ == "__main__":
    plot()