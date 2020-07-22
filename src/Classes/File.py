from Classes.Cell import Cell
import numpy as np
import pandas as pd
import sys
from RuntimeConstants.Runtime_Datasets import TimeFrameColumns
import logging
from Services.Config.Configuration import Config
import datetime
from pathlib import Path
import os
from sklearn.preprocessing import MinMaxScaler
from RuntimeConstants import Runtime_Folders
from Services.FileManagement import Folder_Management


class File:
    def __init__(self, full_name: str):
        self.full_name = full_name
        self.path = self.path = Path(Config.DATA_RAW_DIRECTORY, full_name)
        self.name = os.path.splitext(full_name)[0]
        # The folder where all results are stored in
        self.folder = Folder_Management.create_directory(
            Path(f"{Runtime_Folders.EVALUATION_DIRECTORY}/{self.name}"))
        self.data = self.__load_data()
        self.cells = self.__populate_cells()
        self.total_detected_minutes = self.__get_minutes()

        self.threshold = 0
        # Stimulation time frames. eg. 250 , 450, 640
        self.stimulation_time_frames = list()
        self.total_spikes_per_minutes = list()
        self.total_spikes_per_minute_mean = list()

    def __load_data(self):
        """
        Reads the content of the given file into a pandas data frame
        """
        try:
            return pd.read_csv(self.path, sep="\t", header=0)
        except FileNotFoundError as ex:
            logging.error(f'Could not locate File {self.path}')
            logging.error(ex)
            sys.exit(21)

    def __populate_cells(self):
        """
        Creates cells given by the file
        """

        cells = []
        for column in self.data.columns:
            if column == "Err" or column == "Average":
                continue

            cell = Cell(column)
            # Create time frames
            data = {TimeFrameColumns.TIME_FRAME_VALUE.value: self.data[column]}
            df = pd.DataFrame(data)
            df[TimeFrameColumns.TIME_FRAME_VALUE.value] = pd.to_numeric(df[TimeFrameColumns.TIME_FRAME_VALUE.value])
            # Create including minute column
            df[TimeFrameColumns.INCLUDING_MINUTE.value] = np.floor(
                df[TimeFrameColumns.TIME_FRAME_VALUE.value].index.values * 3.9 / 60)
            df[TimeFrameColumns.ABOVE_THRESHOLD.value] = False

            # Add df to member
            cell.time_frames = df

            # Add cell to df
            cells.append(cell)

        return cells

    def __get_minutes(self):
        """
        Calculates the total amount of minutes
        """
        return len(self.cells[0].time_frames) * 3.9 / 60

    def calculate_baseline_mean(self):
        """
         Calculates the baseline mean
        """
        logging.info('Calculation Baseline Mean....')
        for cell in self.cells:
            cell.baseline_mean = np.average(cell.time_frames[TimeFrameColumns.TIME_FRAME_VALUE.value])
            if Config.VERBOSE:
                logging.info(f'Baseline Mean for Cell {cell.name} -> {cell.baseline_mean}')

        logging.info('Baseline Mean Calculation done.')

    def normalize_time_frames_with_baseline(self):
        """
         Normalize each Timeframe in Cell
        :return:
        """

    # logging.log('Normalize Timeframes with Baseline Mean...')
    # temp_tf_values = []

    # for cell in self.cells:
    #  for timeframe in cell.time_frames[:self.stimulation_time_frames[0]]:
    #       temp_tf_values.append(timeframe.value)

    # mean = np.mean(temp_tf_values)

    # for timeframe in cell.time_frames:
    #   cell.normalized_time_frames.append(
    #      Timeframe(timeframe.identifier, timeframe.value / mean, timeframe.including_minute,
    #                            timeframe.above_threshold))
    #
    #       logging.info('Normalization done.')

    def normalize_time_frames_with_to_ones(self):
        """
        Normalize each Timeframe in Cell with to One Algorithm
        :return:
        """
        logging.info('Normalize Timeframes with To One Method...')

        scaler = MinMaxScaler()

        for cell in self.cells:
            maxValue = cell.time_frames[TimeFrameColumns.TIME_FRAME_VALUE.value].max()

            data = {TimeFrameColumns.TIME_FRAME_VALUE.value: cell.time_frames[
                                                                 TimeFrameColumns.TIME_FRAME_VALUE.value] / maxValue}
            df = pd.DataFrame(data)
            df[TimeFrameColumns.TIME_FRAME_VALUE.value] = pd.to_numeric(df[TimeFrameColumns.TIME_FRAME_VALUE.value])

            # Create including minute column
            df[TimeFrameColumns.INCLUDING_MINUTE.value] = cell.time_frames[TimeFrameColumns.INCLUDING_MINUTE.value]
            df[TimeFrameColumns.ABOVE_THRESHOLD.value] = cell.time_frames[TimeFrameColumns.ABOVE_THRESHOLD.value]

            cell.normalized_time_frames = df

        logging.info('Normalization done.')

    def calculate_time_frame_maximum(self):
        """
        Calculates the timeframe maximum
        :return:
        """
        logging.info('Detecting Timeframe maximum....')
        for cell in self.cells:
            cell.time_frame_maximum = cell.normalized_time_frames[TimeFrameColumns.TIME_FRAME_VALUE.value].max()
            if Config.VERBOSE:
                logging.info(f'Maximum for Cell {cell.name} -> {cell.time_frame_maximum}')

        logging.info('Detecting Timeframe maximum done.')

    def calculate_threshold(self):
        """
          Calculates the Threshold
        :return:
        """
        logging.info('Calculation Threshold...')
        for cell in self.cells:
            cell.threshold = cell.time_frame_maximum * self.threshold
            logging.info(
                'Threshold for Cell {0} -> {1}'.format(cell.name, cell.threshold))

        logging.info('Threshold calculation done.')

    def detect_above_threshold(self):
        """
         Detects if a timeframe is above or below threshold
        :return:
        """
        logging.info(
            'Detecting Timeframe is above or below Threshold...')
        for cell in self.cells:
            cell.normalized_time_frames.loc[
                cell.normalized_time_frames['Value'] < float(
                    cell.threshold), TimeFrameColumns.ABOVE_THRESHOLD.value] = False
            cell.normalized_time_frames.loc[
                cell.normalized_time_frames['Value'] >= float(
                    cell.threshold), TimeFrameColumns.ABOVE_THRESHOLD.value] = True
        logging.info('Detecting done.')

    def count_high_intensity_peaks_per_minute(self):
        """
         Counts high intensity peaks per minute
        :return:
        """
        logging.info('Counting High Intensity Peaks...')
        for cell in self.cells:
            df = cell.normalized_time_frames.groupby(TimeFrameColumns.INCLUDING_MINUTE.value)[
                TimeFrameColumns.ABOVE_THRESHOLD.value].apply(
                lambda x: (x == True).sum()).reset_index()

            del df[TimeFrameColumns.INCLUDING_MINUTE.value]
            df.columns = ['Count']
            cell.high_intensity_counts = df

        logging.info('Counting High Intensity Peaks done.')

    def summarize_high_intensity_peaks(self):
        """
        Summarize all high intensity peaks for all cells for every minute. row wise
        :return:
        """
        logging.info('Summarizing High Intensity Peaks...')
        spikes_per_min: list = [0] * int(self.total_detected_minutes + 1)
        for cell in self.cells:
            for index, row in cell.normalized_time_frames.iterrows():
                if row[TimeFrameColumns.ABOVE_THRESHOLD.value]:
                    spikes_per_min[int(row[TimeFrameColumns.INCLUDING_MINUTE.value])] = spikes_per_min[int(
                        row[TimeFrameColumns.INCLUDING_MINUTE.value])] + 1

        self.total_spikes_per_minutes = spikes_per_min

        for spikes_per_minute in self.total_spikes_per_minutes:
            self.total_spikes_per_minute_mean.append(spikes_per_minute / len(self.cells))

        logging.info('Summarizing High Intensity Peaks done.')

    def split_cells(self):
        """Splitting the cells into intervals using the given time frames"""
        logging.info('Splitting Cells...')
        for cell in self.cells:
            cell.split_cells(self.stimulation_time_frames)
        logging.info('Splitting done.')

    def calculate_high_stimulus_count_per_interval(self):
        """
        Compare the amount of high stimulus in each interval for each cell
        """
        logging.info('Comparing intervals...')
        for cell in self.cells:
            cell.calculate_high_stimulus_count_per_interval()
        logging.info('Interval comparison done.')

    def interval_comparison(self):
        pass

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

        return file_folder

    def generate_report(self):
        """
        Generate all report files
        """
        self.__write_high_stimulus_counts_per_minute()
        self.__write_normalized_time_frames()
        self.__write_total_high_intensity_peaks_per_minute_per_cell()
        logging.info("All reports generated")

    def __write_high_stimulus_counts_per_minute(self):
        """
        Write high stimulus counts per minute
        """

        self.__get_high_stimulus_counts().to_csv(
            os.path.join(self.folder, f"{Config.OUTPUT_FILE_NAME_HIGH_STIMULUS}.csv"), index=None, sep='\t', mode='a')

    def __write_normalized_time_frames(self):
        """
         Write normalized time frames to a file
        :return:
        """
        self.__get_normalized_time_frames().to_csv(
            os.path.join(self.folder, f"{Config.OUTPUT_FILE_NAME_NORMALIZED_DATA}.csv"), index=None, sep='\t', mode='a')

    def __write_total_high_intensity_peaks_per_minute_per_cell(self):
        """
        Write spikes per minutes to a file
        :return:
        """

        minutes = np.arange(int(self.total_detected_minutes) + 1)

        temp_dict = {"Minutes": minutes, "Total spikes": self.total_spikes_per_minutes,
                     " Mean spikes": self.total_spikes_per_minute_mean}

        data_matrix = pd.DataFrame(temp_dict)
        data_matrix.to_csv(os.path.join(self.folder, f"{Config.OUTPUT_FILE_NAME_SPIKES_PER_MINUTE}.csv"), index=None,
                           sep='\t', mode='a')

    def __get_normalized_time_frames(self):
        data = []
        columns = []

        for cell in self.cells:
            columns.append(cell.name)

        for cell in self.cells:
            data.append(cell.normalized_time_frames[TimeFrameColumns.TIME_FRAME_VALUE.value].to_string(index=False))

        data = [i.split('\n') for i in data]

        for li in data:
            li = [float(i) for i in li]

        df = pd.DataFrame(data)
        df = df.T
        df.columns = columns
        return df

    def __get_high_stimulus_counts(self):
        data = []
        columns = []

        for cell in self.cells:
            columns.append(cell.name)

        for cell in self.cells:
            data.append(cell.high_intensity_counts['Count'].to_string(index=False))

        data = [i.split('\n') for i in data]

        for li in data:
            li = [int(i) for i in li]

        df = pd.DataFrame(data)
        df = df.T
        df.columns = columns
        return df
