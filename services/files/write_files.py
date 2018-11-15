import os.path
from enum import Enum


class Paths(Enum):
    SAMPLE_DIR = 'sampleData/'
    INPUT_DIR = 'Input/'
    OUTPUT_DIR = 'Output/'
    OUTPUT_FILE_NAME = 'Results.txt'
    OUTPUT_PATH = 'Output/Results.txt'


def write_file(cell_data):
    file_exists = os.path.exists(Paths.OUTPUT_PATH.value)

    print(file_exists)
    if file_exists:
        os.remove(Paths.OUTPUT_PATH.value)

    fh = open(Paths.OUTPUT_PATH.value, "w")
    written_columns = 0

    for cell in cell_data:
        temp = 'ID: %s :  Mean: %d ' % (cell.id, cell.mean)
        fh.write(temp)
        written_columns += 1
    fh.close()

    print('Creating File %s' % Paths.OUTPUT_PATH.value)
    print('Written Columns: ', written_columns)
