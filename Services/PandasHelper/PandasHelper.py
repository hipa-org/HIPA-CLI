from Classes import InputFile
import pandas as pd


def get_normalized_time_frames(file: InputFile):
    data = []
    columns = []

    for cell in file.cells:
        columns.append(cell.name)

    for cell in file.cells:
        data.append(cell.normalized_time_frames['Value'].to_string(index=False))

    data = [i.split('\n') for i in data]

    for li in data:
        li = [float(i) for i in li]

    df = pd.DataFrame(data)
    df = df.T
    df.columns = columns
    return df


def get_high_stimulus_counts(file: InputFile):
    data = []
    columns = []

    for cell in file.cells:
        columns.append(cell.name)

    for cell in file.cells:
        data.append(cell.high_intensity_counts['Count'].to_string(index=False))

    data = [i.split('\n') for i in data]

    for li in data:
        li = [int(i) for i in li]

    df = pd.DataFrame(data)
    df = df.T
    df.columns = columns
    return df


def get_