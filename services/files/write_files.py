import os.path
from enum import Enum
import numpy as np


class Paths(Enum):
    SAMPLE_DIR = 'sampleData/'
    INPUT_DIR = 'Input/'
    OUTPUT_DIR = 'Output/'
    OUTPUT_FILE_NAME = 'Results.txt'
    OUTPUT_PATH = 'Output/Results.txt'
    LOG_PATH = 'Logs/Log.txt'


def write_results_file(cells):
    file_exists = os.path.exists(Paths.OUTPUT_PATH.value)

    if file_exists:
        os.remove(Paths.OUTPUT_PATH.value)

    temp_array = []
    for cell in cells:
        cell.high_stimulus_per_minute.insert(0, cell.name)
        temp_array.append(cell.high_stimulus_per_minute)

    fh = open(Paths.OUTPUT_PATH.value, "w")

    data = np.array(temp_array)
    data = data.T
    # here you transpose your data, so to have it in two columns

    np.savetxt(Paths.OUTPUT_PATH.value, data, fmt='%s', delimiter='\t')
    fh.close()

    print('Created File %s' % Paths.OUTPUT_PATH.value)


def write_log(message):
    file = open(Paths.LOG_PATH.value, "a")
    file.write(message)
    file.close()
