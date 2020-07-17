from Classes.Cell import Cell
from Classes.TimeFrame import Timeframe
import math
from Services.Logger import Log
import numpy as np
import pandas as pd
import sys
from GlobalData.Statics import TimeFrameColumns


class InputFile:
    def __init__(self, identifier: int, path: str, folder: str, name: str, percentage_limit: float, cells: list,
                 total_detected_minutes: int,
                 content, stimulation_time_frames: list,
                 total_spikes_per_minute: list, total_spikes_per_minute_mean: list):
        self.id = identifier
        self.path = path
        self.folder = folder
        self.name = name
        self.percentage_limit = percentage_limit
        self.cells = cells
        self.total_detected_minutes = total_detected_minutes
        self.content = content
        self.stimulation_time_frames = stimulation_time_frames
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
            if i == "Err" or i == "Average":
                continue

            cell = Cell(i, list(), 0, 0, list(), 0, list(), list(), list())
            # Create time frames
            data = {TimeFrameColumns.VALUE.value: self.content[i]}
            df = pd.DataFrame(data)
            df[TimeFrameColumns.VALUE.value] = pd.to_numeric(df[TimeFrameColumns.VALUE.value])

            # Create including minute column
            df[TimeFrameColumns.INCLUDING_MINUTE.value] = np.floor(
                df[TimeFrameColumns.VALUE.value].index.values * 3.9 / 60)
            df[TimeFrameColumns.ABOVE_THRESHOLD.value] = False

            # Add df to member
            cell.time_frames = df
            # Add cell to list
            cells.append(cell)
            self.cells = cells
        return

    def calculate_minutes(self):
        """
        Calculates the total amount of minutes
        """
        self.total_detected_minutes = len(self.cells[0].time_frames) * 3.9 / 60

    def calculate_baseline_mean(self):
        """
         Calculates the baseline mean
        """
        Log.write_message('Calculation Baseline Mean....', Log.LogLevel.Info)
        for cell in self.cells:
            cell.baseline_mean = np.average(cell.time_frames[TimeFrameColumns.VALUE.value])
            Log.write_message('Baseline Mean for Cell {0} -> {1}'.format(cell.name, cell.baseline_mean),
                              Log.LogLevel.Debug)

        Log.write_message('Baseline Mean Calculation done.', Log.LogLevel.Info)

    def normalize_time_frames_with_baseline(self):
        """
         Normalize each Timeframe in Cell
        :return:
        """
        Log.write_message('Normalize Timeframes with Baseline Mean...', Log.LogLevel.Info)
        temp_tf_values = []

        for cell in self.cells:
            for timeframe in cell.time_frames[:self.stimulation_time_frames[0]]:
                temp_tf_values.append(timeframe.value)

            mean = np.mean(temp_tf_values)

            for timeframe in cell.time_frames:
                cell.normalized_time_frames.append(
                    Timeframe(timeframe.identifier, timeframe.value / mean, timeframe.including_minute,
                              timeframe.above_threshold))

        Log.write_message('Normalization done.', Log.LogLevel.Info)

    def normalize_time_frames_with_to_ones(self):
        """
        Normalize each Timeframe in Cell with to One Algorithm
        :return:
        """
        Log.write_message('Normalize Timeframes with To One Method...', Log.LogLevel.Info)

        for cell in self.cells:
            maxValue = cell.time_frames[TimeFrameColumns.VALUE.value].max()

            data = {TimeFrameColumns.VALUE.value: cell.time_frames[TimeFrameColumns.VALUE.value] / maxValue}
            df = pd.DataFrame(data)
            df[TimeFrameColumns.VALUE.value] = pd.to_numeric(df[TimeFrameColumns.VALUE.value])

            # Create including minute column
            df[TimeFrameColumns.INCLUDING_MINUTE.value] = cell.time_frames[TimeFrameColumns.INCLUDING_MINUTE.value]
            df[TimeFrameColumns.ABOVE_THRESHOLD.value] = cell.time_frames[TimeFrameColumns.ABOVE_THRESHOLD.value]

            cell.normalized_time_frames = df

        Log.write_message('Normalization done.', Log.LogLevel.Info)

    def calculate_time_frame_maximum(self):
        """
        Calculates the timeframe maximum
        :return:
        """
        Log.write_message('Detecting Timeframe maximum....', Log.LogLevel.Info)
        for cell in self.cells:
            cell.time_frame_maximum = cell.normalized_time_frames[TimeFrameColumns.VALUE.value].max()
            Log.write_message('Maximum for Cell {0} -> {1}'.format(cell.name, cell.time_frame_maximum),
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
            cell.threshold = cell.time_frame_maximum * self.percentage_limit
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
            cell.normalized_time_frames.loc[
                cell.normalized_time_frames['Value'] < float(
                    cell.threshold), TimeFrameColumns.ABOVE_THRESHOLD.value] = False
            cell.normalized_time_frames.loc[
                cell.normalized_time_frames['Value'] >= float(
                    cell.threshold), TimeFrameColumns.ABOVE_THRESHOLD.value] = True
        Log.write_message('Detecting done.', Log.LogLevel.Info)

    def count_high_intensity_peaks_per_minute(self):
        """
         Counts high intensity peaks per minute
        :return:
        """
        Log.write_message('Counting High Intensity Peaks...', Log.LogLevel.Info)
        for cell in self.cells:
            df = cell.normalized_time_frames.groupby(TimeFrameColumns.INCLUDING_MINUTE.value)[
                TimeFrameColumns.ABOVE_THRESHOLD.value].apply(
                lambda x: (x == True).sum()).reset_index()

            del df[TimeFrameColumns.INCLUDING_MINUTE.value]
            df.columns = ['Count']
            cell.high_intensity_counts = df

        Log.write_message('Counting High Intensity Peaks done.', Log.LogLevel.Info)

    def summarize_high_intensity_peaks(self):
        """
        Summarize all high intensity peaks for all cells for every minute. row wise
        :return:
        """
        Log.write_message('Summarizing High Intensity Peaks...', Log.LogLevel.Info)
        spikes_per_min: list = [0] * int(self.total_detected_minutes + 1)
        for cell in self.cells:
            for index, row in cell.normalized_time_frames.iterrows():
                if row[TimeFrameColumns.ABOVE_THRESHOLD.value]:
                    spikes_per_min[int(row[TimeFrameColumns.INCLUDING_MINUTE.value])] = spikes_per_min[int(
                        row[TimeFrameColumns.INCLUDING_MINUTE.value])] + 1

        self.total_spikes_per_minutes = spikes_per_min

        for spikes_per_minute in self.total_spikes_per_minutes:
            self.total_spikes_per_minute_mean.append(spikes_per_minute / len(self.cells))

        Log.write_message('Summarizing High Intensity Peaks done.', Log.LogLevel.Info)

    def split_cells(self):
        """Splitting the cells into intervals using the given time frames"""
        Log.write_message('Splitting Cells...', Log.LogLevel.Info)
        for cell in self.cells:
            cell.split_cells(self.stimulation_time_frames)
        Log.write_message('Splitting done.', Log.LogLevel.Info)

    def calculate_high_stimulus_count_per_interval(self):
        """
        Compare the amount of high stimulus in each interval for each cell
        """
        Log.write_message('Comparing intervals...', Log.LogLevel.Info)
        for cell in self.cells:
            cell.calculate_high_stimulus_count_per_interval()
        Log.write_message('Interval comparison done.', Log.LogLevel.Info)

    def interval_comparison(self):
        pass

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
