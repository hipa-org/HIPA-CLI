from Shared.Classes.Cell import Cell
import numpy as np
import pandas as pd
import sys
from CLI.RuntimeConstants.Runtime_Datasets import TimeFrameColumns
import logging
from Shared.Services.Configuration import Configuration_Service
from pathlib import Path
import os
from CLI.RuntimeConstants import Runtime_Folders
from Shared.Services.FileManagement import Folder_Management
import seaborn as sns

sns.set()


class File:
    def __init__(self, path: Path):
        try:
            # TODO: Remove preload for web application
            config = Configuration_Service.get_config()
            self.path = path
            self.name = os.path.splitext(path)[0]
            # The folder where all results are stored in
            self.folder = Folder_Management.create_directory(
                Path(f"{Runtime_Folders.EVALUATION_DIRECTORY}/{self.name}"))

            # Loads the data of the file
            self.data = self.__load_data()

            # Populates the cells
            self.cells = self.__populate_cells()
            # the total detected minutes
            self.total_detected_minutes = self.__get_minutes()

            self.threshold = 0
            # Stimulation time frames. eg. 250 , 450, 640
            self.stimulation_time_frames = []
            self.total_spikes_per_minutes = []
            self.total_spikes_per_minute_mean = []

        except BaseException as ex:
            logging.exception(ex)

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

            # Create cell
            cell = Cell(column)

            # Create initial time frames
            time_frames = pd.DataFrame(
                columns=[f'{TimeFrameColumns.TIME_FRAME_VALUE.value}', f'{TimeFrameColumns.INCLUDING_MINUTE.value}',
                         f'{TimeFrameColumns.ABOVE_THRESHOLD.value}'],
                data={TimeFrameColumns.TIME_FRAME_VALUE.value: self.data[column]})

            # Convert data to numeric
            time_frames[TimeFrameColumns.TIME_FRAME_VALUE.value] = pd.to_numeric(
                time_frames[TimeFrameColumns.TIME_FRAME_VALUE.value])
            # Create including minute column
            time_frames[TimeFrameColumns.INCLUDING_MINUTE.value] = np.floor(
                time_frames[TimeFrameColumns.TIME_FRAME_VALUE.value].index.values * 3.9 / 60)
            time_frames[TimeFrameColumns.ABOVE_THRESHOLD.value] = False

            # Add df to member
            cell.time_frames = time_frames
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
        config = Configuration_Service.get_config()
        logging.info('Calculation Baseline Mean....')
        for cell in self.cells:
            cell.baseline_mean = np.average(cell.time_frames[TimeFrameColumns.TIME_FRAME_VALUE.value])
            if config.GeneralConfig.DEBUG:
                logging.info(f'Baseline Mean for Cell {cell.name} -> {cell.baseline_mean}')

        logging.info('Baseline Mean Calculation done.')

    def normalize_time_frames_with_to_ones(self):
        """
        Normalize each time frame in Cell with to One Algorithm
        :return:
        """
        logging.info('Normalize time frames with To One Method...')

        for cell in self.cells:
            max_value = cell.time_frames[TimeFrameColumns.TIME_FRAME_VALUE.value].max()

            # Create normalized time frames
            time_frames = pd.DataFrame(
                columns=[f'{TimeFrameColumns.TIME_FRAME_VALUE.value}', f'{TimeFrameColumns.INCLUDING_MINUTE.value}',
                         f'{TimeFrameColumns.ABOVE_THRESHOLD.value}'],
                data={TimeFrameColumns.TIME_FRAME_VALUE.value: cell.time_frames[
                                                                   TimeFrameColumns.TIME_FRAME_VALUE.value] / max_value})

            time_frames[TimeFrameColumns.TIME_FRAME_VALUE.value] = pd.to_numeric(
                time_frames[TimeFrameColumns.TIME_FRAME_VALUE.value])

            # Create including minute column
            time_frames[TimeFrameColumns.INCLUDING_MINUTE.value] = cell.time_frames[
                TimeFrameColumns.INCLUDING_MINUTE.value]
            time_frames[TimeFrameColumns.ABOVE_THRESHOLD.value] = cell.time_frames[
                TimeFrameColumns.ABOVE_THRESHOLD.value]

            cell.normalized_time_frames = time_frames

        logging.info('Normalization done.')

    def calculate_time_frame_maximum(self):
        """
        Calculates the time frame maximum
        :return:
        """
        config = Configuration_Service.get_config()
        logging.info('Detecting time frame maximum....')
        for cell in self.cells:
            cell.time_frame_maximum = cell.normalized_time_frames[TimeFrameColumns.TIME_FRAME_VALUE.value].max()
            if config.GeneralConfig.DEBUG:
                logging.info(f'Maximum for cell {cell.name} -> {cell.time_frame_maximum}')

        logging.info('Detecting time frame maximum done.')

    def calculate_threshold(self):
        """
          Calculates the Threshold
        :return:
        """
        config = Configuration_Service.get_config()
        logging.info('Calculation threshold...')
        for cell in self.cells:
            cell.threshold = cell.time_frame_maximum * self.threshold

            if config.GeneralConfig.DEBUG:
                logging.info(f"Threshold for cell {cell.name} -> {cell.threshold}")

        logging.info('Threshold calculation done.')

    def detect_above_threshold(self):
        """
         Detects if a time frame is above or below threshold
        :return:
        """
        logging.info(
            'Detecting time frame is above or below threshold...')
        for cell in self.cells:
            cell.normalized_time_frames.loc[
                cell.normalized_time_frames[TimeFrameColumns.TIME_FRAME_VALUE.value] < float(
                    cell.threshold), TimeFrameColumns.ABOVE_THRESHOLD.value] = False
            cell.normalized_time_frames.loc[
                cell.normalized_time_frames[TimeFrameColumns.TIME_FRAME_VALUE.value] >= float(
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
        """
        Splitting the cells into intervals using the given time frames
        """

        logging.info('Splitting cells...')
        for cell in self.cells:
            cell.create_intervals(self.stimulation_time_frames)
        logging.info('Splitting done.')

    def calculate_high_stimulus_count_per_interval(self):
        """
        Compare the amount of high stimulus in each interval for each cell
        """
        logging.info('Comparing intervals...')
        for cell in self.cells:
            cell.calculate_high_stimulus_count(False)
            cell.calculate_high_stimulus_count(True)
        logging.info('Interval comparison done.')

    def get_folder(self) -> str:
        """
        Returns the base path of the file
        """
        return os.path.basename(self.path)

    def generate_reports(self):
        """
        Generate all report files
        """
        self.__generate_high_stimulus_counts_per_minute_report()
        self.__generate_normalized_time_frames_report()
        self.__generate_total_high_intensity_peaks_per_minute_per_cell_report()
        self.__generate_cell_interval_activation_previous_interval_report()
        self.__generate_cell_interval_activation_to_baseline_report()
        logging.info("All reports generated")

    def generate_plots(self):
        """Generate all plots"""
        pass

    def __generate_cell_interval_activation_to_baseline_report(self):
        """
        Generates the cell interval activation report where activations are
        compared to the base interval
        """
        df = pd.DataFrame()
        for cell in self.cells:
            df[cell.name] = cell.interval_high_intensity_counts_compared_to_baseline['Activation']

        df = df.T
        activations = []
        for column in df.columns:
            column = pd.Series(df[column].values)
            counts = column.value_counts()
            try:
                activations.append(counts[1])
            except KeyError:
                activations.append(0)

        df = df.T
        df['Activations'] = activations
        # df['Activations'] = df[]
        df.to_csv(Path.joinpath(self.folder, "interval_activation_compared_to_baseline_interval.csv"))

    def __generate_cell_interval_activation_previous_interval_report(self):
        """
        Generates the cell interval activation report where activations are
        compared to the previous interval
        """
        df = pd.DataFrame()
        for cell in self.cells:
            df[cell.name] = cell.interval_high_intensity_counts_previous_interval['Activation']

        df = df.T
        activations = []
        for column in df.columns:
            column = pd.Series(df[column].values)
            counts = column.value_counts()
            try:
                activations.append(counts[1])
            except KeyError:
                activations.append(0)

        df = df.T
        df['Activations'] = activations
        # df['Activations'] = df[]
        df.to_csv(Path.joinpath(self.folder, "interval_activation_compared_to_previous_interval.csv"))

    def __generate_high_stimulus_counts_per_minute_report(self):
        """
        Write high stimulus counts per minute
        """
        config = Configuration_Service.get_config()
        data = []
        columns = []

        for cell in self.cells:
            columns.append(cell.name)

        for cell in self.cells:
            data.append(cell.high_intensity_counts['Count'].values)

        df = pd.DataFrame(data)
        df = df.T
        df.columns = columns

        # Export to csv
        df.to_csv(
            os.path.join(self.folder, f"{config.DataConfig.OUTPUT_FILE_NAME_HIGH_STIMULUS}.csv"), index=None, sep='\t', mode='a')

    def __generate_normalized_time_frames_report(self):
        """
         Write normalized time frames to a file
        :return:
        """
        config = Configuration_Service.get_config()
        data = []
        columns = []

        for cell in self.cells:
            columns.append(cell.name)

        for cell in self.cells:
            data.append(cell.normalized_time_frames[TimeFrameColumns.TIME_FRAME_VALUE.value].values)

        df = pd.DataFrame(data)
        df = df.T
        df.columns = columns

        # Export to csv
        df.to_csv(
            os.path.join(self.folder, f"{config.DataConfig.OUTPUT_FILE_NAME_NORMALIZED_DATA}.csv"), index=None, sep='\t', mode='a')

    def __generate_total_high_intensity_peaks_per_minute_per_cell_report(self):
        """
        Write spikes per minutes to a file
        :return:
        """
        config = Configuration_Service.get_config()
        minutes = np.arange(int(self.total_detected_minutes) + 1)

        temp_dict = {"Minutes": minutes, "Total spikes": self.total_spikes_per_minutes,
                     "Mean spikes": self.total_spikes_per_minute_mean}

        data_matrix = pd.DataFrame(temp_dict)
        data_matrix.to_csv(os.path.join(self.folder, f"{config.DataConfig.OUTPUT_FILE_NAME_SPIKES_PER_MINUTE}.csv"), index=None,
                           sep='\t', mode='a')
