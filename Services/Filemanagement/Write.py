import numpy as np

from Services.Logger.Log import write_message, LogLevel
from Services.Config.Config import Config
from Classes import InputFile
import datetime


def high_intensity_counts(file: InputFile):
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
        filename = '{0} {1} {2}{3}'.format(Config.OUTPUT_FILE_NAME_HIGH_STIMULUS, file.name,
                                           now.strftime("%Y-%m-%d %H-%M-%S"), '.txt')
        np.savetxt(
            '{0}{1}'.format(Config.WORKING_DIRECTORY, filename), data, fmt='%s', delimiter='\t')
        write_message(
            'Created File {0} in {1}'.format(filename, Config.WORKING_DIRECTORY), LogLevel.Info)
    except FileNotFoundError as ex:
        write_message('Error creating File!', LogLevel.Error)
        write_message(ex, LogLevel.Error)


def normalized_timeframes(file: InputFile):
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
        filename = '{0} {1} {2}{3}'.format(Config.OUTPUT_FILE_NAME_NORMALIZED_DATA, file.name,
                                           now.strftime("%Y-%m-%d %H-%M-%S"), '.txt')
        np.savetxt(
            '{0}{1}'.format(Config.WORKING_DIRECTORY, filename), data, fmt='%s', delimiter='\t')
        write_message(
            'Created File {0} in {1}'.format(filename, Config.WORKING_DIRECTORY), LogLevel.Info)
    except FileNotFoundError as ex:
        write_message('Error creating File!', LogLevel.Error)
        write_message(ex, LogLevel.Error)
