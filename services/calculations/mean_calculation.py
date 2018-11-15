import numpy as np


def calculate_norm_mean(max_iterations, time_frame):
    new_time_frame = []
    for time_frame_data in time_frame[1:max_iterations+1]:
        new_time_frame.append(float(time_frame_data))
    return np.mean(new_time_frame)


def calculate_mean(time_frame):
    return np.mean(time_frame)
