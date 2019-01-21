from Classes.InputFile import InputFile
from Classes.TimeFrame import Timeframe
import math


class Cell:
    def __init__(self, name, timeframes, threshold, baseline_mean, normalized_timeframes, timeframe_maximum,
                 high_intensity_counts):
        self.name = name
        self.timeframes = timeframes
        self.baseline_mean = baseline_mean
        self.timeframe_maximum = timeframe_maximum
        self.normalized_timeframes = normalized_timeframes
        self.threshold = threshold
        self.high_intensity_counts = high_intensity_counts


def create_cells(file: InputFile):
    cells = list()
    for index, item in enumerate(file.content):
        cell = Cell("", list(), 0, 0, 0, 0, 0)
        timeframes = list()
        identifier = 0
        for element in item:
            if identifier == 0:
                cell.name = element
                identifier += 1
            else:
                timeframes.append(Timeframe(identifier, float(element), math.floor(identifier * 3.9 / 60), 0))
                identifier += 1

        cell.timeframes = timeframes
        cells.append(cell)
        file.cells = cells
    return
