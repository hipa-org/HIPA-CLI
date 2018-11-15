import os.path
from enum import Enum
import numpy as np


class Paths(Enum):
    SAMPLE_DIR = 'sampleData/'
    INPUT_DIR = 'Input/'
    OUTPUT_DIR = 'Output/'
    OUTPUT_FILE_NAME = 'Results.txt'
    OUTPUT_PATH = 'Output/Results.txt'


def write_file(given_data_array):
    file_exists = os.path.exists(Paths.OUTPUT_PATH.value)

    if file_exists:
        os.remove(Paths.OUTPUT_PATH.value)

    fh = open(Paths.OUTPUT_PATH.value, "w")
    written_columns = 0

    print(given_data_array[0])
    data = np.array(given_data_array)
    print(data)
    data = data.T
    # here you transpose your data, so to have it in two columns

    np.savetxt(Paths.OUTPUT_PATH.value, data, fmt='%s', delimiter='\t')
    fh.close()

    print('Creating File %s' % Paths.OUTPUT_PATH.value)
    print('Written Columns: ', written_columns)
