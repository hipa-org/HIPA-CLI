import services
from services.logger.log import write_message, LogLevel
import sys


class PlotValue:
    def __init__(self, id, number):
        self.id = id
        self.number = number


def read_plot_values_file(file_name):
    if services.config.config.Config.DEBUG:
        plot_values = open("sampleData/plot_values.txt", "r").read().splitlines()
    else:
        plot_values = open('Input/{0}.txt'.format(file_name), "r").read().splitlines()

    plot_value_array = []
    split_plot_value_array = []

    for i in plot_values:
        split_plot_value_array.append((i.split('\t', 1)))

    for i in split_plot_value_array:
        plot_value_array.append(PlotValue(i[0], i[1]))

    return plot_value_array


def read_time_traces_file(file_name):
    time_traces_file_data = any
    if services.config.config.Config.DEBUG:
        try:
            time_traces_file_data = open("sampleData/time_traces.txt", "r")
        except ValueError as ex:
            write_message('Could not locate File sampleData/time_traces.txt', LogLevel.Error)
            write_message('More Information in Log', LogLevel.Error)
            write_message(ex, LogLevel.Verbose)
            input()
            sys.exit(21)
    else:
        try:
            time_traces_file_data = open('Input/{0}.txt'.format(file_name), "r")
        except ValueError as ex:
            write_message('Could not locate File sampleData/time_traces.txt', LogLevel.Error)
            write_message('More Information in Log', LogLevel.Error)
            write_message(ex, LogLevel.Verbose)
            input()
            sys.exit(21)

    rows = (row.strip().split() for row in time_traces_file_data)
    time_traces = zip(*(row for row in rows if row))
    time_traces_file_data.close()
    return time_traces
