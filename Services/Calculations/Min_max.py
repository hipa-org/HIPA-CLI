import numpy as np
from Classes import InputFile
from Services.Logger import Log


def calculate_timeframe_maximum(file: InputFile):
    Log.write_message('Detecting Timeframe maximum....', Log.LogLevel.Info)
    for cell in file.cells:
        temp_tf_values = []
        for timeframe in cell.normalized_timeframes:
            temp_tf_values.append(timeframe.value)

        else:
            Log.write_message('Maximum for Cell {0} -> {1}'.format(cell.name, np.max(temp_tf_values)),
                              Log.LogLevel.Verbose)
            cell.timeframe_maximum = np.max(temp_tf_values)

    Log.write_message('Detecting Timeframe maximum done.', Log.LogLevel.Info)


def calculate_threshold(file: InputFile):
    Log.write_message('Calculation Threshold...', Log.LogLevel.Info)
    for cell in file.cells:
        cell.threshold = cell.timeframe_maximum * file.percentage_limit
        Log.write_message('Threshold for Cell {0} -> {1}'.format(cell.name, cell.threshold), Log.LogLevel.Verbose)

    Log.write_message('Threshold calculation done.', Log.LogLevel.Info)
