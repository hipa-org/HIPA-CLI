import numpy as np
from services.logger.log import write_message, LogLevel
from services.config.config import Config
import datetime


def write_results_file(cells, filename):
    now = datetime.datetime.now()
    temp_array = []
    for cell in cells:
        cell.high_stimulus_per_minute.insert(0, cell.name)
        temp_array.append(cell.high_stimulus_per_minute)

    data = np.array(temp_array)
    data = data.T
    try:
        filename = '{0} {1} {2}{3}'.format(Config.OUTPUT_FILE_NAME, filename,
                                           now.strftime("%Y-%m-%d %H-%M-%S"), '.txt')
        np.savetxt(
            '{0}{1}'.format(Config.WORKING_DIRECTORY, filename), data, fmt='%s', delimiter='\t')
        write_message(
            'Created File {0} in {1}'.format(filename, Config.WORKING_DIRECTORY), LogLevel.Info)
    except FileNotFoundError as ex:
        write_message('Error creating File!', LogLevel.Error)
        write_message(ex, LogLevel.Error)
