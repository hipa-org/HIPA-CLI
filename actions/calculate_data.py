import services
from classes import Cell
import inquirer
import datetime
from services.logger.log import LogLevel, write_message
from services.config.config import Config
import os
from clint.textui import puts, colored, indent

cell_data = []
from pyfiglet import Figlet

'''
Main Calculation Function
'''


def calculate_action():
    clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
    clear()

    f = Figlet(font='slant')
    print(f.renderText('High Intensity Peak Analysis'))
    questions = [
        inquirer.Text('file_name', message="Filename"),
        inquirer.Text('time_frame', message="Time Frame"),

        # inquirer.Text('input_path', message="Input Path. Change only i you want to change the Dir"),
        # inquirer.Text('output_path', message="Output Path.  Change only i you want to change the Dir")
    ]
    answers = inquirer.prompt(questions)

    stimulation_time_frame = 0
    file_name = answers['file_name']
    if file_name == '':
        write_message('No Filename given. Using default: {0}'.format(Config.DEFAULT_INPUT_FILE_NAME), LogLevel.Warn)
        file_name = Config.DEFAULT_INPUT_FILE_NAME

    try:
        stimulation_time_frame = int(answers['time_frame'])
    except ValueError as ex:
        write_message(ex, LogLevel.Warn)
        write_message('Value could not converted to a valid Integer Value', LogLevel.Warn)
        input("Press Enter to continue...")
        calculate_action()

    calculate_data(file_name, stimulation_time_frame)


def calculate_data(file_name, stimulation_time_frame):
    start_time = datetime.datetime.now()

    write_message('Input Filename: {0}'.format(file_name), LogLevel.Verbose)
    time_traces = services.files.read_files.read_time_traces_file(file_name)
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

    end_time = datetime.datetime.now()
    write_message('Calculation done in {0} seconds'.format(end_time - start_time), LogLevel.Verbose)


'''
Create a Time Frame Array from the data read by the given File
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
    write_message('Detected {0} Columns including Avg and Err'.format(data_count[0]), LogLevel.Info)
    write_message('Detected {0} Rows excluding the Header Row'.format(data_count[1]), LogLevel.Info)
    write_message('Detected {0} Minutes '.format(minutes), LogLevel.Info)
    return data_count


'''
KAYA SHOULD WROTE SOMETHING HERE
'''


def baseline_mean_calculation(time_frames, stimulation_time_frame):
    write_message('Starting Baseline Mean Calculation....', LogLevel.Info)
    for time_frame in time_frames:
        cal_baseline_mean = services.calculations.mean_calculation.calculate_norm_mean(stimulation_time_frame,
                                                                                       time_frame)

        write_message(
            'Baseline Mean Calculation of Cell {0} finished: -> Baseline Mean {1}'.format(time_frame[0],
                                                                                          cal_baseline_mean),
            LogLevel.Verbose)
        cell_data.append(Cell.Cell(time_frame[0], cal_baseline_mean, 0, 0, 0, 0, 0))
    write_message('Baseline Mean Calculation done', LogLevel.Info)


'''
Calculate the mean. Normalised Cells will be provided
'''


def calculate_mean(normalised_cells):
    write_message('Starting Mean Calculation...', LogLevel.Info)
    index = 0
    for normalised_cell in normalised_cells:
        mean = services.calculations.mean_calculation.calculate_mean(normalised_cell[1:])
        cell_data[index].mean = mean
        index += 1
    write_message('Mean Calculation done', LogLevel.Info)


'''
Calculate the Maximum from given Data Set. 
'''


def maximum_detection(normalised_cells):
    write_message('Detecting Maximum ....', LogLevel.Info)
    index = 0
    for normalised_cell in normalised_cells:
        cell_max = services.calculations.min_max.calculate_maximum(normalised_cell[1:])
        cell_data[index].maximum = cell_max
        index += 1
    write_message('Maximum Detection done', LogLevel.Info)


'''
Calculate Limit for each Cell
'''


def calculate_limit():
    write_message('Calculating Limit...', LogLevel.Info)
    index = 0
    for cell in cell_data:
        sixty_percent_of_maximum = services.calculations.min_max.calculate_limit_from_maximum(cell.maximum)
        cell_data[index].limit = sixty_percent_of_maximum
        index += 1
    write_message('Calculating Limit done', LogLevel.Info)


'''
Check if a data entry of a given cell is over or under the cells limit
'''


def over_under_limit(normalised_cells):
    write_message('Calculating Over and Under Limit...', LogLevel.Info)
    index = 0
    over_under_limit_raw_data = services.calculations.min_max.calculate_over_and_under(normalised_cells, cell_data)
    for over_under_cell_data in over_under_limit_raw_data:
        cell_data[index].over_under_limit = over_under_cell_data[1:]
        index += 1
    write_message('Calculating Over and Under Limit done', LogLevel.Info)


'''
Calculates high stimulus frames per cell 
'''


def calculate_high_stimulus_per_minute(row_count):
    write_message('Calculation High Stimulus per Minute per Cell...', LogLevel.Info)
    temp_over_under_limit = []
    for cell in cell_data:
        temp_over_under_limit.append(cell.over_under_limit)

    high_stimulus_per_minute = services.calculations.high_stimulous.calculate_high_stimulus_per_minute(
        temp_over_under_limit, row_count)
    index = 0
    for high_stimulus_per_cell in high_stimulus_per_minute:
        # print(high_stimulus_per_cell)
        cell_data[index].high_stimulus_per_minute = high_stimulus_per_cell
        index += 1
    write_message('Calculation High Stimulus per Minute per Cell done', LogLevel.Info)
