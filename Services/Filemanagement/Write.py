import numpy as np
from Services.Logger.Log import write_message, LogLevel
from Services.Config.Config import Config
from Classes import InputFile
import datetime


def high_stimulus_file(file: InputFile):
    now = datetime.datetime.now()
    temp_array = []
    for cell in file.cells:
        print(cell.name)

        temp_array.append(cell.name)
        for key, value in cell.high_intensity_counts.items():
            temp_array.append(value)

        data = np.array(temp_array)

        for item in data:
            print(item)
        # data = data.T

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


'''
now = datetime.datetime.now()
    temp_array = []
    for cell in cells:
        cell.high_stimulus_per_minute.insert(0, cell.name)
        temp_array.append(cell.high_stimulus_per_minute)

    data = np.array(temp_array)
    data = data.T
    try:
        filename = '{0} {1} {2}{3}'.format(Config.OUTPUT_FILE_NAME_HIGH_STIMULUS, filename,
                                           now.strftime("%Y-%m-%d %H-%M-%S"), '.txt')
        np.savetxt(
            '{0}{1}'.format(Config.WORKING_DIRECTORY, filename), data, fmt='%s', delimiter='\t')
        write_message(
            'Created File {0} in {1}'.format(filename, Config.WORKING_DIRECTORY), LogLevel.Info)
    except FileNotFoundError as ex:
        write_message('Error creating File!', LogLevel.Error)
        write_message(ex, LogLevel.Error)
'''


def normalized_data(cells, filename):
    now = datetime.datetime.now()
    temp_array = []
    for cell in cells:
        cell.normalized_data.insert(0, cell.name)
        temp_array.append(cell.normalized_data)

    data = np.array(temp_array)
    data = data.T
    try:
        filename = '{0} {1} {2}{3}'.format(Config.OUTPUT_FILE_NAME_NORMALIZED_DATA, filename,
                                           now.strftime("%Y-%m-%d %H-%M-%S"), '.txt')
        np.savetxt(
            '{0}{1}'.format(Config.WORKING_DIRECTORY, filename), data, fmt='%s', delimiter='\t')
        write_message(
            'Created File {0} in {1}'.format(filename, Config.WORKING_DIRECTORY), LogLevel.Info)
    except FileNotFoundError as ex:
        write_message('Error creating File!', LogLevel.Error)
        write_message(ex, LogLevel.Error)
