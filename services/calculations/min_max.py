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
    for frame in range(frame_count + 1):
        print(frame)
        if float(temp_minute) < float(1.0):
            frame_minute.append(frame)
            temp_minute = temp_minute + 0.065
            print('Aktuelle: {0}'.format(temp_minute))
        else:
            frame_minutes.append(frame_minute)
            print('Old {0}'.format(temp_minute))
            temp_minute = temp_minute + 0.065 - 1
            print('Tempminute {0}'.format(temp_minute))
            print('Added new Minute')
            frame_minute = [frame]

    else:
        if temp_minute != 0.065:
            x = temp_minute / 0.065
            print('Ich bin x: {0}'.format(int(x)))
            print(temp_minute)
            frame_minutes.append(frame_minute)

    for minute in frame_minutes:
        frame_minutes_length.append(len(minute))

    print(frame_minutes_length)

    minute_index = 0
    ones_per_minute = []
    for over_under_data in over_under:
        count = 0
        ones_per_minute_cell = []
        cell_index = 0
        for cell in over_under_data[1:]:
            if cell_index < frame_minutes_length[minute_index]:
                if cell == 1:
                    count += 1
                    cell_index += 1
                else:
                    ones_per_minute_cell.append(0)
                    cell_index += 1
            else:
                print(ones_per_minute_cell)
                ones_per_minute.append(ones_per_minute_cell)
                cell_index = 0
                count = 0
                minute_index += 1
        else:
            print('Added new Minute')



''' else:
     print(over_under_data[1:])
     print(ones_per_minute[0])
     print(len(ones_per_minute[0]))
'''

'''stop = 15
ones_per_minute_complete_cells = []
for over_under_set in over_under:
    one_count = 0
    itr_index = 0
    frame_number = 0
    minute = 0
    ones_per_minute_cell_set = []
    for over_under_data in over_under_set[1:]:
        if frame_number == stop:
            print('Cell {0} has in Minute {1} this amount of ones: {2} '.format(over_under_set[0], minute, one_count))
            ones_per_minute_cell_set.append(one_count)
            one_count = 0
            frame_number = 0
            minute += 1
        if int(over_under_data) == 1:
            one_count += 1
            itr_index += 1
        frame_number += 1
    else:
        ones_per_minute_complete_cells.append(ones_per_minute_cell_set)

return ones_per_minute_complete_cells '''
