from Classes import InputFile, TimeFrame
import math


class Cell:
    def __init__(self, name: str, timeframes: list, threshold: float, baseline_mean: float, normalized_timeframes: list,
                 timeframe_maximum: float, high_intensity_counts: dict):
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
        cell = Cell("", list(), 0, 0, list(), 0, {})
        timeframes = list()
        identifier = 0
        for element in item:
            if identifier == 0:
                cell.name = element
                identifier += 1
            else:
                timeframes.append(TimeFrame.Timeframe(identifier, float(element), math.floor(identifier * 3.9 / 60), False))
                identifier += 1

        cell.timeframes = timeframes
        cells.append(cell)
        file.cells = cells
    return
