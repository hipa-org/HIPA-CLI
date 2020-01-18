import numpy as np
import datetime
from Services.Config import Config
from Services.Logger import Log
from Classes import InputFile
import pandas as pd
from Services.PandasHelper import PandasHelper


def high_stimulus_counts_per_minute(file: InputFile):
    now = datetime.datetime.now()

    filename = file.folder + Config.Config.OUTPUT_FILE_NAME_HIGH_STIMULUS + "-" + now.strftime(
        "%Y-%m-%d %H-%M-%S") + ".txt"

    PandasHelper.get_high_stimulus_counts(file).to_csv(filename, index=None, sep='\t', mode='a')
    Log.write_message(
        'Created File {0} in {1}'.format(filename, file.folder), Log.LogLevel.Info)


def normalized_time_frames(file: InputFile):
    """
     Write normalized time frames to a file
    :return:
    """
    now = datetime.datetime.now()
    filename = file.folder + Config.Config.OUTPUT_FILE_NAME_NORMALIZED_DATA + "-" + now.strftime(
        "%Y-%m-%d %H-%M-%S") + ".txt"
    PandasHelper.get_normalized_time_frames(file).to_csv(filename, index=None, sep='\t', mode='a')
    Log.write_message(
        'Created File {0} in {1}'.format(filename, file.folder), Log.LogLevel.Info)


def total_high_intensity_peaks(file: InputFile):
    """
    Write spikes per minutes to a file
    :return:
    """
    now = datetime.datetime.now()
    filename = '{0}_{1}{2}'.format(Config.Config.OUTPUT_FILE_NAME_SPIKES_PER_MINUTE,
                                   now.strftime("%Y-%m-%d %H-%M-%S"), '.txt')

