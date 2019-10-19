import numpy as np
import datetime
from Services.Config import Config
from Services.Logger import Log
from Classes import InputFile


def write_high_intensity_counts(file: InputFile):
    """
    Write high intensity counts to a file
    :return:
    """
    now = datetime.datetime.now()
    file_data = []
    for cell in file.cells:
        temp_array = []
        temp_array.append(cell.name)

        for key, value in cell.high_intensity_counts.items():
            temp_array.append(value)

        file_data.append(temp_array)

    data = np.array(file_data)
    data = data.T

    try:
        filename = '{0}_{1}{2}'.format(Config.Config.OUTPUT_FILE_NAME_HIGH_STIMULUS,
                                       now.strftime("%Y-%m-%d %H-%M-%S"), '.txt')
        np.savetxt(
            '{0}/{1}'.format(file.folder, filename), data, fmt='%s', delimiter='\t')
        Log.write_message(
            'Created File {0} in {1}'.format(filename, file.folder), Log.LogLevel.Info)
    except FileNotFoundError as ex:
        Log.write_message('Error creating File!', Log.LogLevel.Error)
        Log.write_message(ex, Log.LogLevel.Error)


def write_normalized_timeframes(file: InputFile):
    """
     Write normalized timeframes to a file
    :return:
    """
    now = datetime.datetime.now()
    file_data = []
    for cell in file.cells:
        temp_array = []
        temp_array.append(cell.name)

        for timeframe in cell.normalized_timeframes:
            temp_array.append(timeframe.value)

        file_data.append(temp_array)

    data = np.array(file_data)
    data = data.T
    try:
        filename = '{0}_{1}{2}'.format(Config.Config.OUTPUT_FILE_NAME_NORMALIZED_DATA,
                                       now.strftime("%Y-%m-%d %H-%M-%S"), '.txt')
        np.savetxt(
            '{0}/{1}'.format(file.folder, filename), data, fmt='%s', delimiter='\t')
        Log.write_message(
            'Created File {0} in {1}'.format(filename, file.folder), Log.LogLevel.Info)
    except FileNotFoundError as ex:
        Log.write_message('Error creating File!', Log.LogLevel.Error)
        Log.write_message(ex, Log.LogLevel.Error)


def write_total_high_intensity_peaks_per_minute(file: InputFile):
    """
     Write spikes per minutes to a file
    :return:
    """
    now = datetime.datetime.now()
    file_data = []

    # TODO: Change calculation according to new algorithm below.
    # Iterate over each cell and summarize it. Then only only colum output is expected

    minute: int = 0
    for spikes_per_minute in file.total_spikes_per_minutes:
        file_data.append(f"{minute} : {spikes_per_minute}")
        minute += 1

    data = np.array(file_data)
    data = data.T
    try:
        filename = '{0}_{1}{2}'.format(Config.Config.OUTPUT_FILE_NAME_SPIKES_PER_MINUTE,
                                       now.strftime("%Y-%m-%d %H-%M-%S"), '.txt')
        np.savetxt(
            '{0}/{1}'.format(file.folder, filename), data, fmt='%s', delimiter='\t')
        Log.write_message(
            'Created File {0} in {1}'.format(filename, file.folder), Log.LogLevel.Info)
    except FileNotFoundError as ex:
        Log.write_message('Error creating File!', Log.LogLevel.Error)
        Log.write_message(ex, Log.LogLevel.Error)
