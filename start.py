import re

import itertools
import sys
from random import randint
import argparse
import services
from pyfiglet import Figlet
import numpy as np

class Cell:

    def __init__(self, cell_id, baseline_mean, all_mean, maximum, sixty_percent):
        self.cell_id = cell_id
        self.baseline_mean = baseline_mean
        self.mean = all_mean
        self.maximum = maximum
        self.sixty_percent = sixty_percent


ap = argparse.ArgumentParser()
ap.add_argument("-T", "--time", required=True,
                help="the timeFrame")
args = vars(ap.parse_args())
stimulation_time_frame = int(args["time"])

# f = Figlet(font='slant')
# print f.renderText('Calculator')


CellData = []
time_frames = []
time_traces = services.files.read_files.read_time_traces_file()
cell1, cell2 = itertools.tee(CellData, 2)

for time_frame in time_traces:
    time_frame_array = []
    for time_frame_data in time_frame:
        time_frame_array.append(time_frame_data)
    else:
        time_frames.append(time_frame_array)

time_frames1, time_frames2, time_frames3 = itertools.tee(time_frames, 3)

data_count = services.calculations.detectDataSizes.detect_row_and_column_count(time_frames)
minutes = services.calculations.detectDataSizes.calculate_minutes(data_count[1])

print('Detected {0} Columns including Avg and Err'.format(data_count[0]))
print('Detected {0} Rows excluding the Header Row'.format(data_count[1]))
print('Detected {0} Minutes '.format(minutes))
for time_frame in time_frames2:
    cal_baseline_mean = services.calculations.mean_calculation.calculate_norm_mean(stimulation_time_frame, time_frame)
    print(
        'Baseline Mean Calculation of Cell {0} finished: -> Baseline Mean {1}'.format(time_frame[0], cal_baseline_mean))
    CellData.append(Cell(time_frame[0], cal_baseline_mean, 0, 0, 0))

print('Baseline Mean Calculation done')

normalised_cells = services.calculations.normalisation.normalise_columns(CellData, time_frames3)
print('Cell Normalization done')

normalised_cells1, normalised_cells2, normalised_cells3 = itertools.tee(
    normalised_cells, 3)

index = 0
for normalised_cell in normalised_cells1:
    mean = services.calculations.mean_calculation.calculate_mean(normalised_cell[1:])
    CellData[index].mean = mean
    index += 1

print('Mean Calculation done')

index = 0
for normalised_cell in normalised_cells2:
    cell_max = services.calculations.min_max.calculate_maximum(normalised_cell[1:])
    CellData[index].maximum = cell_max
    index += 1

print('Maximum Detection done')

index = 0
for cell in cell1:
    sixty_percent_of_maximum = services.calculations.min_max.calculate_sixty_percent_of_maximum(cell.maximum)
    CellData[index].sixty_percent = sixty_percent_of_maximum
    index += 1
print('Calculating Limit Value done')

over_under = services.calculations.min_max.calculate_over_and_under(normalised_cells3, CellData)
print('Calculating Over and Under Limit done')

ones_per_minute = services.calculations.min_max.cal_one_per_minute(over_under, data_count[1])
print('Calculating Ones per Minutes done')


services.files.write_files.write_file(ones_per_minute)

# services.plot.plot.test_plotting(ones_per_minute)
