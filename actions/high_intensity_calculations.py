from classes import Cell
import inquirer
import datetime
from services.logger.log import write_message, LogLevel
from services.config.config import Config
from services.filemanagement.read_files import read_time_traces_file
from services.filemanagement.write_files import write_results_file
from services.calculations import normalisation, mean_calculation, min_max, high_stimulous, detectDataSizes
import os
from pyfiglet import Figlet
import re

cell_data = []

'''
Main Calculation Function
'''


def start_high_intensity_calculations():
    clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
    clear()
    f = Figlet(font='slant')
    print(f.renderText('High Intensity Peak Analysis'))

    questions = [
        inquirer.Text('working_dir', message="Working Dir (Leave blank for config default"),
        inquirer.Text('time_frame', message="Time Frame"),
    ]
    answers = inquirer.prompt(questions)

    stimulation_time_frame = 0

    global cell_data
    cell_data = []
    try:
        stimulation_time_frame = int(answers['time_frame'])
    except ValueError as ex:
        write_message(ex, LogLevel.Warn)
        write_message('Value could not converted to a valid Integer Value', LogLevel.Warn)
        input("Press Enter to continue...")
        start_high_intensity_calculations()
        return

    working_dir = answers['working_dir']
    if working_dir == '':
        write_message('No Working Directory given. Using default: {0}'.format(Config.DEFAULT_WORKING_DIRECTORY),
                      LogLevel.Warn)
        working_dir = Config.DEFAULT_WORKING_DIRECTORY
    else:
        char_index = 0
        for char in working_dir:
            if char_index == len(working_dir) - 1:
                if char is not '/':
                    line = re.sub('[ ]', '', working_dir)
                    working_dir = '{0}{1}'.format(line, '/')
            char_index += 1

    write_message('Using Directory: {0}'.format(working_dir), LogLevel.Info)

    all_files = os.listdir(working_dir)
    temp_files = []
    for file in all_files:
        if Config.DEFAULT_INPUT_FILE_NAME in file:
            temp_files.append(file)

    files = [
        inquirer.List('file_name',
                      message="Choose Input File",
                      choices=temp_files,
                      )
    ]

    chosen_file = inquirer.prompt(files)
    file_name = chosen_file['file_name']
    write_message('Stimulated Time Frame: {}'.format(stimulation_time_frame), LogLevel.Verbose)
    execute_high_intensity_calculation(file_name, stimulation_time_frame)
    return True


def execute_high_intensity_calculation(file_name, stimulation_time_frame):
    start_time = datetime.datetime.now()

    write_message('Input Filename: {0}'.format(file_name), LogLevel.Verbose)
    time_traces = read_time_traces_file(file_name)
    time_frames = create_time_frame_array(time_traces)
    data_count = calculate_provided_data(time_frames)
    baseline_mean_calculation(time_frames, stimulation_time_frame)
    normalised_cells = normalisation.normalise_columns(cell_data, time_frames)
    calculate_mean(normalised_cells)
    maximum_detection(normalised_cells)
    calculate_limit()
    over_under_limit(normalised_cells)
    calculate_high_stimulus_per_minute(data_count[1])
    write_results_file(cell_data)

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
    data_count = detectDataSizes.detect_row_and_column_count(time_frames)
    minutes = detectDataSizes.calculate_minutes(data_count[1])
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
        cal_baseline_mean = mean_calculation.calculate_norm_mean(stimulation_time_frame,
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
        mean = mean_calculation.calculate_mean(normalised_cell[1:])
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
        cell_max = min_max.calculate_maximum(normalised_cell[1:])
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
        sixty_percent_of_maximum = min_max.calculate_limit_from_maximum(cell.maximum)
        cell_data[index].limit = sixty_percent_of_maximum
        index += 1
    write_message('Calculating Limit done', LogLevel.Info)


'''
Check if a data entry of a given cell is over or under the cells limit
'''


def over_under_limit(normalised_cells):
    write_message('Calculating Over and Under Limit...', LogLevel.Info)
    index = 0
    over_under_limit_raw_data = min_max.calculate_over_and_under(normalised_cells, cell_data)
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

    high_stimulus_per_minute = high_stimulous.calculate_high_stimulus_per_minute(
        temp_over_under_limit, row_count)
    index = 0
    for high_stimulus_per_cell in high_stimulus_per_minute:
        # print(high_stimulus_per_cell)
        cell_data[index].high_stimulus_per_minute = high_stimulus_per_cell
        index += 1
    write_message('Calculation High Stimulus per Minute per Cell done', LogLevel.Info)
