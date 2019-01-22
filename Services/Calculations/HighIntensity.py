from Services.Logger import Log
from Classes import InputFile


def detect_above_threshold(file: InputFile):
    Log.write_message('Detecting Timeframe is above or below Threshold...', Log.LogLevel.Info)
    for cell in file.cells:
        for timeframe in cell.normalized_timeframes:
            if float(timeframe.value) >= float(cell.threshold):
                timeframe.above_threshold = True
            else:
                timeframe.above_threshold = False

    Log.write_message('Detecting done.', Log.LogLevel.Info)


def count_high_intensity_peaks_per_minute(file: InputFile):
    Log.write_message('Counting High Intensity Peaks...', Log.LogLevel.Info)
    for cell in file.cells:
        for timeframe in cell.normalized_timeframes:
            if timeframe.including_minute not in cell.high_intensity_counts:
                if timeframe.above_threshold:
                    cell.high_intensity_counts[timeframe.including_minute] =  1
                else:
                    cell.high_intensity_counts[timeframe.including_minute] =  0

            else:
                if timeframe.above_threshold:
                    cell.high_intensity_counts[timeframe.including_minute] = cell.high_intensity_counts[
                                                                                 timeframe.including_minute] + 1
    Log.write_message('Counting High Intensity Peaks done.', Log.LogLevel.Info)