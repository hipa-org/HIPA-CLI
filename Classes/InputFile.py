from Classes import Cell, TimeFrame
import math
from Services.Logger.Log import write_message, LogLevel
import numpy as np
import datetime
import sys
from Services.Config import Config


class InputFile:
    def __init__(self, identifier: int, path: str, folder: str, name: str, percentage_limit: float, cells: list,
                 total_detected_minutes: int,
                 content, stimulation_timeframes: list,
                 total_spikes_per_minute: list):
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

    def calculate_minutes(self):
        self.total_detected_minutes = len(self.cells[0].timeframes) * 3.9 / 60

    def create_cells(self):
        """
            Creates cells given by the file
        """
        cells = list()
        for index, item in enumerate(self.content):
            cell = Cell.Cell("", list(), 0, 0, list(), 0, {})
            timeframes = list()
            identifier = 0
            for element in item:
                if identifier == 0:
                    cell.name = element
                    identifier += 1
                else:
                    timeframes.append(
                        TimeFrame.Timeframe(identifier, float(element), math.floor(identifier * 3.9 / 60), False))
                    identifier += 1

            cell.timeframes = timeframes
            cells.append(cell)
            self.cells = cells
        return

    def calculate_baseline_mean(self):
        """
         Calculates the baseline mean
        """
        write_message('Calculation Baseline Mean....', LogLevel.Info)
        temp_timeframes = []
        for cell in self.cells:
            for timeframe in cell.timeframes:
                if timeframe.identifier <= self.stimulation_timeframes[0]:
                    temp_timeframes.append(timeframe.value)
            else:
                cell.baseline_mean = np.average(temp_timeframes)
                write_message('Baseline Mean for Cell {0} -> {1}'.format(cell.name, cell.baseline_mean),
                              LogLevel.Verbose)

        write_message('Baseline Mean Calculation done.', LogLevel.Info)

    def calculate_timeframe_maximum(self):
        """
        Calculates the timeframe maximum
        :return:
        """
        write_message('Detecting Timeframe maximum....', LogLevel.Info)
        for cell in self.cells:
            temp_tf_values = []
            for timeframe in cell.normalized_timeframes:
                temp_tf_values.append(timeframe.value)

            else:
                write_message('Maximum for Cell {0} -> {1}'.format(cell.name, np.max(temp_tf_values)),
                              LogLevel.Verbose)
                cell.timeframe_maximum = np.max(temp_tf_values)

        write_message(
            'Detecting Timeframe maximum done.', LogLevel.Info)

    def calculate_threshold(self):
        """
          Calculates the Threshold
        :return:
        """
        write_message('Calculation Threshold...', LogLevel.Info)
        for cell in self.cells:
            cell.threshold = cell.timeframe_maximum * self.percentage_limit
            write_message(
                'Threshold for Cell {0} -> {1}'.format(cell.name, cell.threshold), LogLevel.Verbose)

        write_message('Threshold calculation done.', LogLevel.Info)

    def detect_above_threshold(self):
        """
         Detects if a timeframe is above or below threshold
        :return:
        """
        write_message(
            'Detecting Timeframe is above or below Threshold...', LogLevel.Info)
        for cell in self.cells:
            for timeframe in cell.normalized_timeframes:
                if float(timeframe.value) >= float(cell.threshold):
                    timeframe.above_threshold = True
                else:
                    timeframe.above_threshold = False

        write_message('Detecting done.', LogLevel.Info)

    def count_high_intensity_peaks_per_minute(self):
        """
         Counts high intensity peaks per minute
        :return:
        """
        write_message('Counting High Intensity Peaks...', LogLevel.Info)
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
        write_message('Counting High Intensity Peaks done.', LogLevel.Info)

    def normalize_timeframes_with_baseline(self):
        """
         Normalize each Timeframe in Cell
        :return:
        """
        write_message('Normalize Timeframes with Baseline Mean...', LogLevel.Info)
        temp_tf_values = []

        for cell in self.cells:
            for timeframe in cell.timeframes[:self.stimulation_timeframes[0]]:
                temp_tf_values.append(timeframe.value)

            mean = np.mean(temp_tf_values)

            for timeframe in cell.timeframes:
                cell.normalized_timeframes.append(
                    TimeFrame.Timeframe(timeframe.identifier, timeframe.value / mean, timeframe.including_minute,
                                        timeframe.above_threshold))

        write_message('Normalization done.', LogLevel.Info)

    def normalize_timeframes_with_to_ones(self):
        """
        Normalize each Timeframe in Cell with to One Algorithm
        :return:
        """
        write_message('Normalize Timeframes with To One Method...', LogLevel.Info)

        for cell in self.cells:
            max = 0
            for timeframe in cell.timeframes:
                if timeframe.value >= max:
                    max = timeframe.value

            for timeframe in cell.timeframes:
                cell.normalized_timeframes.append(
                    TimeFrame.Timeframe(timeframe.identifier, timeframe.value / max, timeframe.including_minute,
                                        timeframe.above_threshold))

        write_message('Normalization done.', LogLevel.Info)

    def read_time_traces_file(self):
        try:
            file_content = open('{0}'.format(str(self.path)), "r")
            rows = (row.strip().split() for row in file_content)
            content = zip(*(row for row in rows if row))
            self.content = content
            file_content.close()
        except FileNotFoundError as ex:
            write_message('Could not locate File {0}'.format(self.path),
                          LogLevel.Error)
            write_message(ex, LogLevel.Verbose)
            input()
            sys.exit(21)

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