import numpy as np
from Services.Logger.log import write_message, LogLevel


def calculate_baseline_mean(file):
    write_message('Calculation Baseline Mean....', LogLevel.Info)
    temp_timeframes = []
    for cell in file.cells:
        for timeframe in cell.timeframes:
            if timeframe.identifier <= file.stimulation_timeframe:
                temp_timeframes.append(timeframe.value)
        else:
            cell.baseline_mean = np.average(temp_timeframes)
            write_message('Baseline Mean for Cell {0} -> {1}'.format(cell.name, cell.baseline_mean), LogLevel.Verbose)

    write_message('Baseline Mean Calculation done.', LogLevel.Info)