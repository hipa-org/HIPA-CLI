'''
Normalize each Datapoint in Cell
'''


def normalise_columns(cell_data, time_frames):
    normalized_time_frames = []
    index = 0

    for time_frame in time_frames:
        normalized_time_frame = []
        normalized_time_frame.append(time_frame[0])
        for column in time_frame[1:]:
            normalized_time_frame.append(float(column) / float(cell_data[index].baseline_mean))
        else:
            normalized_time_frames.append(normalized_time_frame)
            index += 1
    else:
        return normalized_time_frames
