import os.path
from enum import Enum
import numpy as np
from services.logger.log import LogLevel, write_message
from services.config.config import Config
import datetime


class Paths(Enum):

    def __str__(self):
        return str(self.value)

    SAMPLE_DIR = 'sampleData/'
    INPUT_DIR = 'Input/'
    OUTPUT_DIR = 'Output/'
    LOG_PATH = 'Log/Log.txt'


def write_results_file(cells):
    now = datetime.datetime.now()
    output_path = '{0}{1}{2}'.format(str(Paths.OUTPUT_DIR), str(Config.DEFAULT_OUTPUT_FILE_NAME), '.txt')
    temp_array = []
    for cell in cells:
        cell.high_stimulus_per_minute.insert(0, cell.name)
        temp_array.append(cell.high_stimulus_per_minute)

    data = np.array(temp_array)
    data = data.T
    print(now.strftime("%Y-%m-%d %H-%M-%S"))
    np.savetxt(
        '{0}{1}-{2}{3}'.format(Paths.OUTPUT_DIR, Config.DEFAULT_OUTPUT_FILE_NAME, now.strftime("%Y-%m-%d %H-%M-%S"),
                               '.txt'), data, fmt='%s', delimiter='\t')
    write_message('Created File in {0}{1}{2}'.format(Paths.OUTPUT_DIR, Config.DEFAULT_OUTPUT_FILE_NAME, '.txt'),
                  LogLevel.Info)
