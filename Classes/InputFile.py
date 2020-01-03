from Classes.Cell import Cell
from Classes.TimeFrame import Timeframe
import math
from Services.Logger import Log
import numpy as np
import pandas as pd
import sys


class InputFile:
    def __init__(self, identifier: int, path: str, folder: str, name: str, percentage_limit: float, cells: list,
                 total_detected_minutes: int,
                 content, stimulation_timeframes: list,
                 total_spikes_per_minute: list, total_spikes_per_minute_mean: list):
        self.id = identifier
        self.path = path
        self.folder = folder
        self.name = name
        self.percentage_limit = percentage_limit
        self.cells = cells
        self.total_detected_minutes = total_detected_minutes
        self.content = content
        self.stimulation_timeframes = stimulation_timeframes
        self.total_spikes_per_minutes = total_spikes_per_minute
        self.total_spikes_per_minute_mean = total_spikes_per_minute_mean

    def read_time_traces_file(self):
        """
        Read the content of the given file into a pandas dataframe
        """
        try:
            df = pd.read_csv(str(self.path), sep="\t", header=0)
            self.content = df
        except FileNotFoundError as ex:
            Log.write_message('Could not locate File {0}'.format(self.path),
                              Log.LogLevel.Error)
            Log.write_message(ex, Log.LogLevel.Verbose)
            input()
            sys.exit(21)

    def create_cells(self):
        """
            Creates cells given by the file
        """

        cells = list()
        for i in self.content.columns:
            cell = Cell(i, list(), 0, 0, list(), 0, {})
            # Create time frames
            data = {'Value': self.content[i]}
            df = pd.DataFrame(data)
            df['Value'] = pd.to_numeric(df['Value'])

            # Create including minute column
            df['IncludingMinute'] = np.floor(df['Value'].index.values * 3.9 / 60)
            df['AboveThreshold'] = False

            # Add df to member
            cell.timeframes = df

            # Add cell to list
            cells.append(cell)
            self.cells = cells
        return

    def calculate_minutes(self):
        """
        Calculates the total amount of minutes
        """
        self.total_detected_minutes = len(self.cells[0].timeframes) * 3.9 / 60

    def calculate_baseline_mean(self):
        """
         Calculates the baseline mean
        """
        Log.write_message('Calculation Baseline Mean....', Log.LogLevel.Info)
        for cell in self.cells:
            cell.baseline_mean = np.average(cell.timeframes['Value'])
            Log.write_message('Baseline Mean for Cell {0} -> {1}'.format(cell.name, cell.baseline_mean),
                              Log.LogLevel.Debug)

        Log.write_message('Baseline Mean Calculation done.', Log.LogLevel.Info)

    def normalize_timeframes_with_baseline(self):
        """
         Normalize each Timeframe in Cell
        :return:
        """
        Log.write_message('Normalize Timeframes with Baseline Mean...', Log.LogLevel.Info)
        temp_tf_values = []

        for cell in self.cells:
            for timeframe in cell.timeframes[:self.stimulation_timeframes[0]]:
                temp_tf_values.append(timeframe.value)

            mean = np.mean(temp_tf_values)

            for timeframe in cell.timeframes:
                cell.normalized_timeframes.append(
                    Timeframe(timeframe.identifier, timeframe.value / mean, timeframe.including_minute,
                              timeframe.above_threshold))

        Log.write_message('Normalization done.', Log.LogLevel.Info)

    def normalize_timeframes_with_to_ones(self):
        """
        Normalize each Timeframe in Cell with to One Algorithm
        :return:
        """
        Log.write_message('Normalize Timeframes with To One Method...', Log.LogLevel.Info)

        for cell in self.cells:
            values = cell.timeframes['Value']
            maxValue = cell.timeframes['Value'].max()

            data = {'Value': cell.timeframes['Value'] / maxValue}
            df = pd.DataFrame(data)
            df['Value'] = pd.to_numeric(df['Value'])

            # Create including minute column
            df['IncludingMinute'] = cell.timeframes['IncludingMinute']
            df['AboveThreshold'] = cell.timeframes['AboveThreshold']

            cell.normalized_timeframes = df

        Log.write_message('Normalization done.', Log.LogLevel.Info)

    def calculate_timeframe_maximum(self):
        """
        Calculates the timeframe maximum
        :return:
        """
        Log.write_message('Detecting Timeframe maximum....', Log.LogLevel.Info)
        for cell in self.cells:
            cell.timeframe_maximum = cell.normalized_timeframes['Value'].max()
            Log.write_message('Maximum for Cell {0} -> {1}'.format(cell.name, cell.timeframe_maximum),
                              Log.LogLevel.Verbose)

        Log.write_message(
            'Detecting Timeframe maximum done.', Log.LogLevel.Info)

    def calculate_threshold(self):
        """
          Calculates the Threshold
        :return:
        """
        Log.write_message('Calculation Threshold...', Log.LogLevel.Info)
        for cell in self.cells:
            cell.threshold = cell.timeframe_maximum * self.percentage_limit
            Log.write_message(
                'Threshold for Cell {0} -> {1}'.format(cell.name, cell.threshold), Log.LogLevel.Debug)

        Log.write_message('Threshold calculation done.', Log.LogLevel.Info)

    def detect_above_threshold(self):
        """
         Detects if a timeframe is above or below threshold
        :return:
        """
        Log.write_message(
            'Detecting Timeframe is above or below Threshold...', Log.LogLevel.Info)
        for cell in self.cells:
            cell.normalized_timeframes.loc[
                cell.normalized_timeframes['Value'] < float(cell.threshold), 'AboveThreshold'] = 'False'
            cell.normalized_timeframes.loc[
                cell.normalized_timeframes['Value'] >= float(cell.threshold), 'AboveThreshold'] = 'True'
        Log.write_message('Detecting done.', Log.LogLevel.Info)

    def count_high_intensity_peaks_per_minute(self):
        """
         Counts high intensity peaks per minute
        :return:
        """
        Log.write_message('Counting High Intensity Peaks...', Log.LogLevel.Info)
        for cell in self.cells:
            for timeframe in cell.normalized_timeframes:
                if timeframe.including_minute not in cell.high_intensity_counts:
                    if timeframe.above_threshold:
                        cell.high_intensity_counts[timeframe.including_minute] = 1
                    else:
                        cell.high_intensity_counts[timeframe.including_minute] = 0

                else:
                    if timeframe.above_threshold:
                        cell.high_intensity_counts[timeframe.including_minute] = cell.high_intensity_counts[
                                                                                     timeframe.including_minute] + 1
        Log.write_message('Counting High Intensity Peaks done.', Log.LogLevel.Info)

    def get_file_name(self):
        """
        Evaluates the file name
        :return:
        """
        path_split = self.path.split(".")
        path_split = path_split[:-1]
        path_split = path_split[0].split("/")
        file_name = path_split[-1]
        self.name = file_name

    def get_folder(self):
        path_split = self.path.split(".")
        path_split = path_split[:-1]
        path_split = path_split[0].split("/")
        path_split = path_split[:-1]
        file_folder = ""
        for path_fragment in path_split:
            if file_folder == "":
                file_folder = path_fragment + "/"
            else:
                file_folder = file_folder + path_fragment + "/"

        self.folder = file_folder

    def summarize_high_intensity_peaks(self):
        """
        Summarize all high intensity peaks for all cells for every minute. row wise
        :return:
        """
        spikes_per_min: list = [0] * int(self.total_detected_minutes + 1)
        for cell in self.cells:
            if cell.name == "Average" or cell.name == "Err":
                continue
            for timeframe in cell.normalized_timeframes:
                if timeframe.above_threshold:
                    spikes_per_min[timeframe.including_minute] = spikes_per_min[timeframe.including_minute] + 1

        self.total_spikes_per_minutes = spikes_per_min

        for spikes_per_minute in self.total_spikes_per_minutes:
            self.total_spikes_per_minute_mean.append(spikes_per_minute / len(self.cells))
