from services.logger.log import write_message, LogLevel


def calculate_high_stimulus_per_minute(over_under_limit_data, frame_count):
    frame_minutes_length = calculate_frames_per_minute(frame_count)
    return collect_all_high_stimulus(over_under_limit_data, frame_minutes_length)


def count_high_stimulus_per_cell_per_minute(cell_data_for_minute, minute):
    count = 0
    write_message('Collected Cell Data {0} for Minute {1}'.format(cell_data_for_minute, minute), LogLevel.Verbose)
    for cell_data in cell_data_for_minute:
        if cell_data == 1:
            count += 1

    return count


def calculate_frames_per_minute(frame_count):
    frame_minute = []
    temp_minute = 0.065
    frame_minutes = []
    frame_minutes_length = []
    for frame in range(frame_count):
        if float(temp_minute) < float(1.0):
            frame_minute.append(frame)

            temp_minute = temp_minute + 0.065
        else:
            write_message('Add new Minute {0}'.format(frame_minute), LogLevel.Debug)
            frame_minutes.append(frame_minute)
            temp_minute = temp_minute + 0.065 - 1
            frame_minute = [frame]

    else:
        write_message('Add new Minute {0}'.format(frame_minute), LogLevel.Debug)
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

    return frame_minutes_length


def collect_all_high_stimulus(over_under_limit_data, frame_minutes_length):
    ones_per_minute_complete = []

    for cells in over_under_limit_data:
        high_stimulus_per_cell = []
        high_stimulus_per_minute = []
        minute_index = 0
        index = 0
        for cell in cells[1:]:
            if len(high_stimulus_per_minute) < frame_minutes_length[minute_index]:
                high_stimulus_per_minute.append(cell)
            else:
                count = count_high_stimulus_per_cell_per_minute(high_stimulus_per_minute, minute_index)
                high_stimulus_per_cell.append(count)
                high_stimulus_per_minute = []
                high_stimulus_per_minute.append(cell)
                minute_index += 1
            index += 1
        else:
            count = count_high_stimulus_per_cell_per_minute(high_stimulus_per_minute, minute_index)
            high_stimulus_per_cell.append(count)
            high_stimulus_per_minute = []
            minute_index += 1
            amount_of_frames_missing = frame_minutes_length[len(frame_minutes_length) - 1]
            if amount_of_frames_missing != 0:
                for cell in cells[len(cells) - amount_of_frames_missing:]:
                    high_stimulus_per_minute.append(cell)
                count = count_high_stimulus_per_cell_per_minute(high_stimulus_per_minute, minute_index)
                high_stimulus_per_cell.append(count)
            ones_per_minute_complete.append(high_stimulus_per_cell)

    else:
        write_message(ones_per_minute_complete, LogLevel.Debug)
        return ones_per_minute_complete
