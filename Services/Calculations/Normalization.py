from Classes import InputFile, TimeFrame
import numpy as np
from Services.Logger import Log

'''
Normalize each Timeframe in Cell
'''


def normalize_timeframes_with_baseline(file: InputFile):
    Log.write_message('Normalize Timeframes with Baseline Mean...', Log.LogLevel.Info)
    temp_tf_values = []

    for cell in file.cells:
        for timeframe in cell.timeframes[:file.stimulation_timeframe]:
            temp_tf_values.append(timeframe.value)

        mean = np.mean(temp_tf_values)

        for timeframe in cell.timeframes:
            cell.normalized_timeframes.append(
                TimeFrame.Timeframe(timeframe.identifier, timeframe.value / mean, timeframe.including_minute,
                                    timeframe.above_threshold))

    Log.write_message('Normalization done.', Log.LogLevel.Info)


def normalize_timeframes_with_to_ones(file: InputFile):
    Log.write_message('Normalize Timeframes with To One Method...', Log.LogLevel.Info)

    for cell in file.cells:
        max = 0
        for timeframe in cell.timeframes:
            if timeframe.value >= max:
                max = timeframe.value

        for timeframe in cell.timeframes:
            cell.normalized_timeframes.append(
                TimeFrame.Timeframe(timeframe.identifier, timeframe.value / max, timeframe.including_minute,
                                    timeframe.above_threshold))

    Log.write_message('Normalization done.', Log.LogLevel.Info)
