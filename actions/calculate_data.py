import services
import itertools
from classes import Cell
import inquirer
import config

cell_data = []

'''
Main Calculation Function
'''


def calculate_data():
    questions = [
        inquirer.Text('time_frame', message="Time Frame"),
        # inquirer.Text('input_path', message="Input Path. Change only i you want to change the Dir"),
        # inquirer.Text('output_path', message="Output Path.  Change only i you want to change the Dir")
    ]
    answers = inquirer.prompt(questions)

    print(answers)

    stimulation_time_frame = int(answers['time_frame'])

    time_traces = services.files.read_files.read_time_traces_file()
    time_frames = create_time_frame_array(time_traces)
    data_count = calculate_provided_data(time_frames)
    baseline_mean_calculation(time_frames, stimulation_time_frame)
    normalised_cells = services.calculations.normalisation.normalise_columns(cell_data, time_frames)
    calculate_mean(normalised_cells)
    maximum_detection(normalised_cells)
    calculate_limit()
    over_under_limit(normalised_cells)
    calculate_high_stimulus_per_minute(data_count[1])
    services.files.write_files.write_results_file(cell_data)


'''
Create a Time Frame Array from the data read by the give File
'''


def create_time_frame_array(time_traces):
    time_frames = []
    for time_frame in time_traces:
        time_frame_array = []
        for time_frame_data in time_frame:
            time_frame_array.append(time_frame_data)
        else:
            time_frames.append(time_frame_array)

    return time_frames


'''
Calculates some basic info for the user. 
'''


def calculate_provided_data(time_frames):
    data_count = services.calculations.detectDataSizes.detect_row_and_column_count(time_frames)
    minutes = services.calculations.detectDataSizes.calculate_minutes(data_count[1])
    print('Detected {0} Columns including Avg and Err'.format(data_count[0]))
    print('Detected {0} Rows excluding the Header Row'.format(data_count[1]))
    print('Detected {0} Minutes '.format(minutes))
    return data_count


'''
KAYA SHOULD WROTE SOMETHING HERE
'''


def baseline_mean_calculation(time_frames, stimulation_time_frame):
    print('Starting Baseline Mean Calculation....')
    for time_frame in time_frames:
        cal_baseline_mean = services.calculations.mean_calculation.calculate_norm_mean(stimulation_time_frame,
                                                                                       time_frame)
        if config.config.verbose_mode:
            print(
                'Baseline Mean Calculation of Cell {0} finished: -> Baseline Mean {1}'.format(time_frame[0],
                                                                                              cal_baseline_mean))
        cell_data.append(Cell.Cell(time_frame[0], cal_baseline_mean, 0, 0, 0, 0, 0))
    print('Baseline Mean Calculation done')


'''
Calculate the mean. Normalised Cells will be provided
'''


def calculate_mean(normalised_cells):
    print('Starting Mean Calculation...')
    index = 0
    for normalised_cell in normalised_cells:
        mean = services.calculations.mean_calculation.calculate_mean(normalised_cell[1:])
        cell_data[index].mean = mean
        index += 1
    print('Mean Calculation done')


'''
Calculate the Maximum from given Data Set. 
'''


def maximum_detection(normalised_cells):
    print('Detecting Maximum ....')
    index = 0
    for normalised_cell in normalised_cells:
        cell_max = services.calculations.min_max.calculate_maximum(normalised_cell[1:])
        cell_data[index].maximum = cell_max
        index += 1
    print('Maximum Detection done')


'''
Calculate Limit for each Cell
'''


def calculate_limit():
    print('Calculating Limit...')
    index = 0
    for cell in cell_data:
        sixty_percent_of_maximum = services.calculations.min_max.calculate_limit_from_maximum(cell.maximum)
        cell_data[index].limit = sixty_percent_of_maximum
        index += 1
    print('Calculating Limit done')


'''
Check if a data entry of a given cell is over or under the cells limit
'''


def over_under_limit(normalised_cells):
    print('Calculating Over and Under Limit...')
    index = 0
    over_under_limit_raw_data = services.calculations.min_max.calculate_over_and_under(normalised_cells, cell_data)
    for over_under_cell_data in over_under_limit_raw_data:
        cell_data[index].over_under_limit = over_under_cell_data[1:]
        index += 1
    print('Calculating Over and Under Limit done')


'''
Calculates high stimulus frames per cell 
'''


def calculate_high_stimulus_per_minute(row_count):
    print('Calculation High Stimulus per Minute per Cell...')
    temp_over_under_limit = []
    for cell in cell_data:
        temp_over_under_limit.append(cell.over_under_limit)

    high_stimulus_per_minute = services.calculations.min_max.calculate_high_stimulus_per_minute(temp_over_under_limit,
                                                                                                row_count)
    index = 0
    for high_stimulus_per_cell in high_stimulus_per_minute:
        # print(high_stimulus_per_cell)
        cell_data[index].high_stimulus_per_minute = high_stimulus_per_cell
        index += 1
    print('Calculation High Stimulus per Minute per Cell done')
