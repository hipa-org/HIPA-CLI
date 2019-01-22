from Classes import InputFile, TimeFrame
import numpy as np
from Services.Logger import Log

'''
Normalize each Timeframe in Cell
'''


def normalize_timeframes(file: InputFile):
    Log.write_message('Normalize Timeframes...', Log.LogLevel.Info)
    temp_tf_values = []

    for cell in file.cells:
        for timeframe in cell.timeframes[:file.stimulation_timeframe]:
            temp_tf_values.append(timeframe.value)

        mean = np.mean(temp_tf_values)

        for timeframe in cell.timeframes:
            #Log.write_message('Normalized Value for Timeframe {0} in Cell {1} -> {2}'.format(timeframe.identifier, cell.name, timeframe.value / mean), Log.LogLevel.Debug)
            cell.normalized_timeframes.append(
                TimeFrame.Timeframe(timeframe.identifier, timeframe.value / mean, timeframe.including_minute,
                                    timeframe.above_threshold))

    Log.write_message('Normalization done.', Log.LogLevel.Info)
