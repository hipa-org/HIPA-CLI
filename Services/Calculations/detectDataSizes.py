from Classes.InputFile import InputFile


def detect_row_and_column_count(file: InputFile):
    data = []
    column_count = 0
    row_count = 0
    for time_frame in file:
        column_count += 1
        row_count = len(time_frame[1:])
    else:
        data.append(column_count)
        data.append(row_count)
        return data


def calculate_minutes(row_count):
    return (row_count * 3.9) / 60
