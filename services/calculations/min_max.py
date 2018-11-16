import numpy as np
import config


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


def calculate_high_stimulus_per_minute(over_under_limit_data, frame_count):
    frame_minute = []
    temp_minute = 0.065
    frame_minutes = []
    frame_minutes_length = []

    for frame in range(frame_count):
        if float(temp_minute) < float(1.0):
            frame_minute.append(frame)

            temp_minute = temp_minute + 0.065
        else:
            frame_minutes.append(frame_minute)
            temp_minute = temp_minute + 0.065 - 1
            frame_minute = [frame]

    else:
        frame_minutes.append(frame_minute)
        temp_minute = temp_minute + 0.065 - 1
        frame_minute = []
        if temp_minute != 0.065:
            x = temp_minute / 0.065
            for count in reversed(range(int(x))):
                frame_minute.append(frame_count - count)

            frame_minutes.append(frame_minute)

    for minute in frame_minutes:
        frame_minutes_length.append(len(minute))

    ones_per_minute_complete = []

    for cells in over_under_limit_data:
        ones_per_minute_cell = []
        ones_per_minute_cell.append(cells[0])
        ones_per_minute = []
        minute_index = 0
        index = 0
        for cell in cells[1:]:
            if len(ones_per_minute) < frame_minutes_length[minute_index]:
                ones_per_minute.append(cell)
            else:
                count = count_cell_ones_per_minute(ones_per_minute, minute_index)
                ones_per_minute_cell.append(count)
                ones_per_minute = []
                ones_per_minute.append(cell)
                minute_index += 1
            index += 1
        else:
            count = count_cell_ones_per_minute(ones_per_minute, minute_index)
            ones_per_minute_cell.append(count)
            ones_per_minute = []
            minute_index += 1
            amount_of_frames_missing = frame_minutes_length[len(frame_minutes_length) - 1]

            for cell in cells[len(cells) - amount_of_frames_missing:]:
                ones_per_minute.append(cell)
            count = count_cell_ones_per_minute(ones_per_minute, minute_index)
            ones_per_minute_cell.append(count)
            ones_per_minute_complete.append(ones_per_minute_cell)

    else:
        '''print(frame_minutes_length)
        print(len(frame_minutes_length))
        print(ones_per_minute_complete[len(ones_per_minute_complete) - 1])
        print(len(ones_per_minute_complete[len(ones_per_minute_complete) - 1])) '''
        return ones_per_minute_complete


def count_cell_ones_per_minute(cell_data_for_minute, minute):
    count = 0
    if config.config.verbose_mode:
        print('Collected Cell Data {0} for Minute {1}'.format(cell_data_for_minute, minute))
    for cell_data in cell_data_for_minute:
        if cell_data == 1:
            count += 1

    return count
