import numpy as np
from services.logger.log import write_message, LogLevel
from services.config.config import Config
import datetime


def write_results_file(cells):
    now = datetime.datetime.now()
    temp_array = []
    for cell in cells:
        cell.high_stimulus_per_minute.insert(0, cell.name)
        temp_array.append(cell.high_stimulus_per_minute)

    data = np.array(temp_array)
    data = data.T
    try:
        np.savetxt(
            '{0}{1}-{2}{3}'.format(Config.DEFAULT_WORKING_DIRECTORY, Config.DEFAULT_OUTPUT_FILE_NAME,
                                   now.strftime("%Y-%m-%d %H-%M-%S"),
                                   '.txt'), data, fmt='%s', delimiter='\t')
        write_message(
            'Created File {0}-{1}{2} in {3}{4}{5}'.format(Config.DEFAULT_OUTPUT_FILE_NAME,
                                                          now.strftime("%Y-%m-%d %H-%M-%S"),
                                                          '.txt', Config.DEFAULT_WORKING_DIRECTORY,
                                                          Config.DEFAULT_OUTPUT_FILE_NAME,
                                                          '.txt'),
            LogLevel.Info)
    except FileNotFoundError as ex:
        write_message('Error creating File!', LogLevel.Error)
        write_message(ex, LogLevel.Error)
