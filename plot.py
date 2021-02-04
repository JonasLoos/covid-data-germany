import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from datetime import date
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


def plot_graph(days, name):
    fig, ax1 = plt.subplots(1, figsize=(12,8))
    fig.suptitle('Covid-cases and -deaths')
    # ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))
    ax1.set_xlabel('date')
    ax1.set_ylim(0,40000)
    # ax1.xaxis.set_major_locator(mdates.DayLocator(interval=n//10))
    ax2 = ax1.twinx()
    ax2.set_ylim(0,2000)

    for x, ax, color in [('cases', ax1, 'blue'), ('deaths', ax2, 'red')]:
        today, = [np.genfromtxt(f'{x}/{day}', delimiter=',', dtype=int) for day in sorted(os.listdir(x))[-1:]]
        data = today[1:,1:].sum(axis=0)
        normal_dates = [date.fromordinal(x) for x in range(today[0,1], today[0,1]+len(today[0,1:]))[-days:]]
        ax.plot(normal_dates, data[-days:], color=color, linestyle='dotted')
        average_days = [date.fromordinal(x) for x in range(today[0,1], today[0,1]+len(today[0,1:])-3)[-days+3:]]
        ax.plot(average_days, average(data)[-days+3:], color=color)
        ax.tick_params(axis='y', labelcolor=color)
        ax.set_ylabel(x, color=color)

    fig.tight_layout()
    plt.savefig(f'plots/{name}.png', dpi=100)



def plot_heatmap(measurement, days, name, log_scale=False):
    fig, ax = plt.subplots(1)
    date_box = [mdates.date2num(date.fromordinal(first_day-366+x)) for x in [-days,days,0,days]]
    if log_scale:
        result += 1  # because log 0 isn't nice
        im = ax.imshow(result, extent=date_box, cmap=plt.get_cmap('inferno'), norm=colors.LogNorm())
    else:
        im = ax.imshow(result, extent=date_box, cmap=plt.get_cmap('inferno'))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))
    ax.yaxis.set_major_formatter(mdates.DateFormatter('%d.%m.'))
    ax.yaxis.set_major_locator(mdates.DayLocator(interval=10))
    plt.gcf().autofmt_xdate()
    ax.set_xlabel('date of the added data')
    ax.set_ylabel('date of publication')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="2%", pad=0.05)
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    plt.colorbar(im, cax=cax)

    fig.suptitle('Added covid-cases in some publications (each compared to the publication on the day before)', fontsize=14)
    plt.figtext(0.5, 0.94, '(date 0 is the day of the first saved publication)', ha='center')
    plt.savefig(f'plots/delay_{name}.png', dpi=100)


if __name__ == "__main__":
    plot_graph(10000, 'new_data_all')
    plot_graph(28, 'new_data_28d')
    # plot_heatmap(10000, 'cases', 'delay_cases_all')
    # plot_heatmap(28, 'cases', 'delay_cases_28d')
    # plot_heatmap(10000, 'deaths', 'delay_deaths_all')
    # plot_heatmap(28, 'deaths', 'delay_deaths_28d')
