import numpy as np
from Services.Logger import Log


def calculate_baseline_mean(file):
    Log.write_message('Calculation Baseline Mean....', Log.LogLevel.Info)
    temp_timeframes = []
    for cell in file.cells:
        for timeframe in cell.timeframes:
            if timeframe.identifier <= file.stimulation_timeframe:
                temp_timeframes.append(timeframe.value)
        else:
            cell.baseline_mean = np.average(temp_timeframes)
            Log.write_message('Baseline Mean for Cell {0} -> {1}'.format(cell.name, cell.baseline_mean),
                              Log.LogLevel.Verbose)

    Log.write_message('Baseline Mean Calculation done.', Log.LogLevel.Info)
