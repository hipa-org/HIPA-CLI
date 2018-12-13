from classes import Cell
import datetime
from services.logger.log import write_message, LogLevel
from services.config.config import Config
from services.filemanagement.read_files import read_time_traces_file
from services.filemanagement.write_files import write_high_stimulus_file, write_normalized_data
from services.calculations import normalisation, mean_calculation, min_max, high_stimulous, detectDataSizes
import os
from pyfiglet import Figlet
import re
from enum import Enum


class OutputOptions(Enum):
    High_Stimulus = 'High Stimulus'
    Normalized_Data = 'Normalized Data'


cell_data = []
files_to_process = []
'''
Main Calculation Function
'''


def start_high_intensity_calculations():
    clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
    clear()
    global files_to_process
    files_to_process = []
    f = Figlet(font='slant')
    print(f.renderText('High Intensity Peak Analysis'))

    user_file_output_option = ask_file_output()
    if len(user_file_output_option) == 0:
        write_message('No Output selected. Calculations will be done, but no Output will be generated', LogLevel.Warn)
    print('-------------')
    working_dir = ask_working_dir()
    print('-------------')
    files_to_process = ask_files_to_process(working_dir)
    if len(files_to_process) == 0:
        write_message('No Files selected.. Aborting', LogLevel.Info)
        return True
    print('-------------')
    write_message(files_to_process, LogLevel.Debug)
    stimulation_time_frames = ask_stimulus_time_frame(files_to_process)
    write_message(stimulation_time_frames, LogLevel.Debug)

    for file in stimulation_time_frames:
        global cell_data
        cell_data = []
        print()
        write_message('Processing file {0}'.format(file['file_name']), LogLevel.Info)
        execute_high_intensity_calculation(file['file_name'], file['stimulation_time_frame'], user_file_output_option)
    return True


'''
Asks the User about the working dir
'''


def ask_working_dir():
    print('Specify the working dir. Leave blank for config default. ')
    print('Custom dir example: sampleData/. This will use the sampleData folder.\n'
          'Custom Dir can be located all over your local machine')
    working_dir = input('Working Dir: ')
    if working_dir == '':
        write_message('No Working Directory given. Using default: {0}'.format(Config.WORKING_DIRECTORY),
                      LogLevel.Warn)
        working_dir = Config.WORKING_DIRECTORY
    else:
        char_index = 0
        for char in working_dir:
            if char_index == len(working_dir) - 1:
                if char is not '/':
                    line = re.sub('[ ]', '', working_dir)
                    working_dir = '{0}{1}'.format(line, '/')
            char_index += 1
        write_message('Using Directory: {0}'.format(working_dir), LogLevel.Info)

    return working_dir


'''
Asks which files should be processed
'''


def ask_file_output():
    chosen_output = []

    print('1. High Stimulus')
    print('2. Normalized Data')
    choose = input('Which files do you want to create? (Type each Number separated by comma)\n')
    chosen_output_answer = choose.split(',')
    for choose in chosen_output_answer:
        if choose.isdigit():
            if int(choose) == 1:
                chosen_output.append(OutputOptions.High_Stimulus.value)
            if int(choose) == 2:
                chosen_output.append(OutputOptions.Normalized_Data.value)

    return chosen_output


'''
Which Files should be processed
'''


def ask_files_to_process(working_dir):
    all_files = os.listdir(os.path.normpath(working_dir))
    temp_files = []
    for file in all_files:
        if Config.INPUT_FILE_NAME in file:
            if Config.OUTPUT_FILE_NAME_HIGH_STIMULUS not in file and Config.OUTPUT_FILE_NAME_NORMALIZED_DATA not in file:
                temp_files.append(file)

    print('Files available: ')
    print()
    i = 0
    for file in temp_files:
        print('{0}: {1}'.format(i, file))
        i += 1

    print()
    chosen_files = []

    choosen_number_input = input(
        'Choose all files you want to process. (Type each number separated by comma or '
        'just press enter to select all files)\n')

    if choosen_number_input == '':
        chosen_files = temp_files
    else:
        for choosen_number in choosen_number_input.split(','):
            if choosen_number.isdigit():
                chosen_files.append(temp_files[int(choosen_number)])

    return chosen_files


def ask_stimulus_time_frame(selected_files):
    stimulation_time_frames = []
    for file in selected_files:
        stimulus_time_frame = input('Frame of stimulation for file {0}: '.format(file))

        if stimulus_time_frame.isdigit():
            stimulation_time_frames.append({'file_name': file,
                                            'stimulation_time_frame': int(stimulus_time_frame)})
        else:
            ask_stimulus_time_frame(files_to_process)

    return stimulation_time_frames


def execute_high_intensity_calculation(file_name, stimulation_time_frame, user_file_output):
    start_time = datetime.datetime.now()
    time_traces = read_time_traces_file(file_name)
    time_frames = create_time_frame_array(time_traces)
    data_count = calculate_provided_data(time_frames)
    baseline_mean_calculation(time_frames, stimulation_time_frame)
    normalized_cells = normalize_cells(cell_data, time_frames)
    calculate_mean(normalized_cells)
    maximum_detection(normalized_cells)
    calculate_limit()
    over_under_limit(normalized_cells)
    calculate_high_stimulus_per_minute(data_count[1])
    for output_option in user_file_output:
        if output_option == OutputOptions.High_Stimulus.value:
            write_high_stimulus_file(cell_data, file_name)
        elif output_option == OutputOptions.Normalized_Data.value:
            write_normalized_data(cell_data, file_name)

    end_time = datetime.datetime.now()
    write_message('Calculation done in {0} seconds.'.format(end_time - start_time), LogLevel.Verbose)
    write_message('{0} data points processed'.format(data_count[0] * data_count[1]), LogLevel.Verbose)


def normalize_cells(cell_data_input, time_frames):
    normalized_data_cells = normalisation.normalise_columns(cell_data_input, time_frames)
    index = 0
    for normalized_data in normalized_data_cells:
        cell_data[index].normalized_data = normalized_data[1:]
        index += 1

    return normalized_data_cells


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
Mean of Intensities before Stimulation
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
        cell_data.append(Cell.Cell(time_frame[0], cal_baseline_mean, 0, 0, 0, 0, 0, 0))
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
