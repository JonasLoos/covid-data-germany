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
    print(f'\r{name}: plotting', end='')
    fig, ax1 = plt.subplots(1, figsize=(6,4))
    fig.suptitle('Covid-cases and -deaths')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y'))
    # ax1.xaxis.set_major_locator(mdates.DayLocator(interval=n//10))
    plt.gcf().autofmt_xdate()
    ax1.set_xlabel('date')
    ax1.set_ylim(0,40000)
    ax2 = ax1.twinx()
    ax2.set_ylim(0,2000)

    for x, ax, color in [('cases', ax1, 'blue'), ('deaths', ax2, 'red')]:
        today, = [np.genfromtxt(f'{x}/{day}', delimiter=',', dtype=int) for day in sorted(os.listdir(x))[-1:]]
        data = today[1:,1:].sum(axis=0)
        normal_dates = [mdates.date2num(date.fromordinal(x)) for x in range(today[0,1], today[0,1]+len(today[0,1:]))[-days:]]
        ax.plot(normal_dates, data[-days:], color=color, linestyle='dotted')
        average_days = [mdates.date2num(date.fromordinal(x)) for x in range(today[0,1], today[0,1]+len(today[0,1:])-3)[-days+3:]]
        ax.plot(average_days, average(data)[-days+3:], color=color)
        ax.tick_params(axis='y', labelcolor=color)
        ax.set_ylabel(x, color=color)

    fig.tight_layout()
    plt.savefig(f'plots/{name}.png', dpi=150)
    print(f'\r{name}: done'+' '*20)


def filename_to_date(file):
    return date(int(file[:4]), int(file[5:7]), int(file[8:10])).toordinal()


def plot_heatmap(days, measurement, name, log_scale=False):
    # read files
    files = sorted(os.listdir(measurement))
    first_file_date = filename_to_date(files[0])
    last_file_date = filename_to_date(files[-1])
    days = min(days, last_file_date-first_file_date+1)
    start_date = last_file_date - days + 1
    data = np.zeros((days, last_file_date - date(2020,1,1).toordinal()))
    for file in files:
        print(f'\r{name}: reading {measurement}/{file}', end='')
        file_date = filename_to_date(file)
        # only read files after start_date
        if file_date >= start_date:
            new_data = np.absolute(np.genfromtxt(f'{measurement}/{file}', delimiter=',', dtype=int)[1:,1:]).sum(axis=0)
            data[last_file_date-file_date,:len(new_data)] = new_data

    # subtract counts from previous day to get changes
    print(f'\r{name}: calculating changes'+' '*20, end='')
    for i in range(days-1):
        if data[i].sum() > 0 and data[i+1].sum() > 0:
            # only do this for valid days with valid yesterdays
            data[i] -= data[i+1]
        else:
            # set it to 0 if not
            data[i] = 0
    data = np.where(data>0, data, 0)  # replace negative values with 0
    # data[:-1] *= (data[1:].sum(axis=1)>0)[:,None]  # set days to 0 where the previous day was 0
    data = data[:-1]  # cut off oldest data, as it cant be compared to anything before
    days -= 1

    # cut data to plottable area
    offset = 28
    data = data[:,-offset-days:]

    # plot
    print(f'\r{name}: creating plot'+' '*20, end='')
    fig, ax = plt.subplots(1, figsize=(6,4))
    date_box = [mdates.date2num(date.fromordinal(start_date+x)) for x in [-offset,days,0,days]]
    if log_scale:
        # data += 1  # because log 0 isn't nice
        im = ax.imshow(data, extent=date_box, cmap=plt.get_cmap('magma'), norm=colors.SymLogNorm(1, base=10))
    else:
        im = ax.imshow(data, extent=date_box, cmap=plt.get_cmap('magma'))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=data.shape[1]//8))
    ax.yaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y'))
    ax.yaxis.set_major_locator(mdates.DayLocator(interval=data.shape[0]//8))
    plt.gcf().autofmt_xdate()
    ax.set_xlabel('date of the added data')
    ax.set_ylabel('date of publication')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="2%", pad=0.05)
    # ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    plt.colorbar(im, cax=cax)

    fig.suptitle(f'Added covid-{measurement} per day')
    fig.tight_layout()
    plt.savefig(f'plots/{name}.png', dpi=150)
    print(f'\r{name}: done'+' '*20)



if __name__ == "__main__":
    plot_graph(28, 'new_data_28d')
    plot_graph(10000, 'new_data_all')
    plot_heatmap(28, 'cases', 'delay_cases_28d')
    plot_heatmap(10000, 'cases', 'delay_cases_all', True)
    plot_heatmap(28, 'deaths', 'delay_deaths_28d')
    plot_heatmap(10000, 'deaths', 'delay_deaths_all', True)
