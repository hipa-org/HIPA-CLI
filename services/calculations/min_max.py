import numpy as np


def calculate_maximum(time_frame):
    detected_max = np.argmax(time_frame)
    return time_frame[detected_max]


def calculate_sixty_percent_of_maximum(maximum):
    return maximum * 0.6


def calculate_over_and_under(normalized_cell_data, cell_data):
    over_under_complete_cells = []
    index = 0

    for time_frame in normalized_cell_data:
        over_under_set = []
        over_under_set.append(time_frame[0])
        for time_frame_data in time_frame[1:]:
            if float(time_frame_data) < float(cell_data[index].sixty_percent):
                over_under_set.append(0)
            else:
                over_under_set.append(1)
        else:
            over_under_complete_cells.append(over_under_set)
            index += 1

    return over_under_complete_cells


def cal_one_per_minute(over_under, frame_count):
    frame_minute = []
    temp_minute = 0.065
    frame_minutes = []
    frame_minutes_length = []
    indexe = 0
    print(frame_count)
    for frame in range(frame_count):
        if float(temp_minute) < float(1.0):
            print(temp_minute)
            frame_minute.append(frame)

            temp_minute = temp_minute + 0.065
            print('Index: {0} mit tempMinute {1}'.format(indexe, temp_minute))
        else:
            print('Else')
            frame_minutes.append(frame_minute)
            temp_minute = temp_minute + 0.065 - 1
            frame_minute = [frame]

        indexe += 1
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

    for cells in over_under:
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
            # print('Reached index {0}'.format(index))
            count = count_cell_ones_per_minute(ones_per_minute, minute_index)
            ones_per_minute_cell.append(count)
            ones_per_minute = []
            minute_index += 1
            amount_of_frames_missing = frame_minutes_length[len(frame_minutes_length) - 1]
            # print('Frames missing {0}'.format(amount_of_frames_missing))
            # print('1400: {0}'.format(cells[1400]))
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
    print('Collected Cell Data {0} for Minute {1}'.format(cell_data_for_minute, minute))
    for cell_data in cell_data_for_minute:
        if cell_data == 1:
            count += 1

    return count
