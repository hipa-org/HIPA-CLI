import numpy as np
from Classes import InputFile


def calculate_timeframe_maximum(file: InputFile):
    for cell in file.cells:
        cell.timeframe_maximum = np.argmax(cell.timeframes)


def calculate_threshold(file: InputFile):
    for cell in file.cells:
        cell.threshold = cell.timeframe_maximum * file.percentage_limit


