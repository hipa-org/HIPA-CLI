import numpy as np


def calculate_timeframe_maximum(time_frame):
    detected_max = np.argmax(time_frame)
    return time_frame[detected_max]


def calculate_threshold_of_timeframe_maximum(timeframe_maximum, percentage_limit):
    return timeframe_maximum * percentage_limit


def detect_above_below_threshold(normalized_timeframes, cell):
    over_under_complete_cells = []
    index = 0

    for time_frame in normalized_cell_data:
        over_under_set = []
        over_under_set.append(time_frame[0])
        for time_frame_data in time_frame[1:]:
            if float(time_frame_data) < float(cell_data[index].limit):
                over_under_set.append(0)
            else:
                over_under_set.append(1)
        else:
            over_under_complete_cells.append(over_under_set)
            index += 1

    return over_under_complete_cells


