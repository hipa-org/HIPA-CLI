import numpy as np


def calculate_maximum(time_frame):
    detected_max = np.argmax(time_frame)
    return time_frame[detected_max]


def calculate_limit_from_maximum(maximum):
    return maximum * 0.6


def calculate_over_and_under(normalized_cell_data, cell_data):
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


