import numpy as np


def calculate_baseline_mean(file):
    temp_timeframes = []
    for cell in file:
        for timeframe in cell.timeframes:
            if timeframe.identifier <= file.stimulation_timeframe:
                temp_timeframes.append(timeframe.value)
        else:
            cell.baseline_mean = np.mean(temp_timeframes)
            

''' new_time_frame = []
 for time_frame_data in time_frame[1:max_iterations+1]:
     new_time_frame.append(float(time_frame_data))
 return np.mean(new_time_frame)'''
