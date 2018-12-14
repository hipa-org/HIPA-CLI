<<<<<<< HEAD
=======
from classes import Cell
>>>>>>> rewrite
import datetime
import os
<<<<<<< HEAD
=======

>>>>>>> rewrite
import re
from enum import Enum
from UI.UI import print_empty_line,  print_hic_headline, print_minus_line

import inquirer
from pyfiglet import Figlet

from classes import Cell
from services.calculations import normalisation, mean_calculation, min_max, high_stimulous, detectDataSizes
from services.config.config import Config
from services.filemanagement.read_files import read_time_traces_file
from services.filemanagement.write_files import write_high_stimulus_file, write_normalized_data
from services.logger.log import write_message, LogLevel
from services.plot.plot import test_plotting


class OutputOptions(Enum):
    High_Stimulus = 'High Stimulus'
    Normalized_Data = 'Normalized Data'


"""
The Cell Data. All Cells are stored as Objects in here
"""
cell_data = []
<<<<<<< HEAD


def start_high_intensity_calculations():
    """
    Main Calculation Function
    :return:
    """
    clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
    clear()
    f = Figlet(font='slant')
    print(f.renderText('High Intensity Peak Analysis'))

=======
files_to_process = []
'''
Main Calculation Function
'''


def start_high_intensity_calculations():
    print_hic_headline()
    global files_to_process
    files_to_process = []
>>>>>>> rewrite
    user_file_output_option = ask_file_output()
    print_minus_line()
    working_dir = ask_working_dir()
    print_minus_line()
    files_to_process = ask_files_to_process(working_dir)
    write_message(files_to_process, LogLevel.Debug)
    stimulation_time_frames = ask_stimulus_time_frame(files_to_process)
    write_message(stimulation_time_frames, LogLevel.Debug)
    for file in stimulation_time_frames:
        global cell_data
        cell_data = []
        print_empty_line()
        write_message('Processing file {0}'.format(file['file_name']), LogLevel.Info)
        execute_high_intensity_calculation(file['file_name'], file['stimulation_time_frame'], user_file_output_option)
    return True


def ask_working_dir():
<<<<<<< HEAD
    """
    Asks the User about the working dir
    :return:
    """
    working_dir_question = [
        inquirer.Text('working_dir', message="Working Dir (Leave blank for config default)"),
    ]
    working_dir_answer = inquirer.prompt(working_dir_question)

    working_dir = working_dir_answer['working_dir']
    if working_dir == '':
=======
    print('Specify the working dir. Leave blank for config default. ')
    print('Custom dir example: sampleData/. This will use the sampleData folder.\n'
          'Custom Dir can be located all over your local machine')
    working_dir = input('Working Dir: ')
    if working_dir.strip() == '':
>>>>>>> rewrite
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


def ask_file_output():
<<<<<<< HEAD
    """
    Asks which files should be processed
    :return:
    """
    output_options = [
        inquirer.Checkbox('output_options',
                          message="Which files do you want to create? (Select with space)",
                          choices=[OutputOptions.High_Stimulus.value, OutputOptions.Normalized_Data.value],
                          ),
    ]
    chosen_output_answer = inquirer.prompt(output_options)
=======
>>>>>>> rewrite
    chosen_output = []
    print('Available Choices:\n')
    print('1. High Stimulus')
    print('2. Normalized Data')
    print('Which files should be created as Output?')
    print('(Type each Number separated by comma or just press enter to select all options!')
    user_choose = input()

    if user_choose.strip() == '':
        chosen_output.append(OutputOptions.High_Stimulus.value)
        chosen_output.append(OutputOptions.Normalized_Data.value)
        return chosen_output

    user_choose = user_choose.split(',')
    for choose in user_choose:
        if choose.isdigit():
            if int(choose.strip()) == 1:
                chosen_output.append(OutputOptions.High_Stimulus.value)
            if int(choose.strip()) == 2:
                chosen_output.append(OutputOptions.Normalized_Data.value)

    if len(chosen_output) == 0:
        write_message('No Output selected. Calculations will be done, but no Output will be generated', LogLevel.Warn)

    return chosen_output


<<<<<<< HEAD
=======
'''
Which Files should be processed
'''


>>>>>>> rewrite
def ask_files_to_process(working_dir):
    """
    Which Files should be processed
    :param working_dir:
    :return:
    """
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

    user_input = input(
        'Choose all files you want to process. (Type each number separated by comma or '
        'just press enter to select all files)\n')

    if user_input.strip() == '':
        chosen_files = temp_files
    else:
        for number in user_input.split(','):
            if number.strip().isdigit():
                chosen_files.append(temp_files[int(number)])

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
    # test_plotting(cell_data)
    write_message('Calculation done in {0} seconds.'.format(end_time - start_time), LogLevel.Verbose)
    write_message('{0} data points processed'.format(data_count[0] * data_count[1]), LogLevel.Verbose)


def normalize_cells(cell_data_input, time_frames):
    normalized_data_cells = normalisation.normalise_columns(cell_data_input, time_frames)
    index = 0
    for normalized_data in normalized_data_cells:
        cell_data[index].normalized_data = normalized_data[1:]
        index += 1

    return normalized_data_cells


def create_time_frame_array(time_traces):
    """
    Create a Time Frame Array from the data read by the given File(s)
    :param time_traces:
    :return:
    """
    time_frames = []
    for time_frame in time_traces:
        time_frame_array = []
        for time_frame_data in time_frame:
            time_frame_array.append(time_frame_data)
        else:
            time_frames.append(time_frame_array)

    for cell in time_frames:
        cell_data.append(Cell.Cell(cell[0], cell[1:], 0, 0, 0, 0, 0, 0, 0))

    for cell in cell_data:
        print(cell.name)
        print(cell.time_frames)
    input('wait')
    return time_frames


def calculate_provided_data(time_frames):
    """
    Calculates some basic info for the user.
    :param time_frames:
    :return:
    """
    data_count = detectDataSizes.detect_row_and_column_count(time_frames)
    minutes = detectDataSizes.calculate_minutes(data_count[1])
    write_message('Detected {0} Columns including Avg and Err'.format(data_count[0]), LogLevel.Info)
    write_message('Detected {0} Rows excluding the Header Row'.format(data_count[1]), LogLevel.Info)
    write_message('Detected {0} Minutes '.format(minutes), LogLevel.Info)
    return data_count


def baseline_mean_calculation(time_frames, stimulation_time_frame):
    """
    Mean of Intensities before Stimulation
    :param time_frames:
    :param stimulation_time_frame:
    :return:
    """
    write_message('Starting Baseline Mean Calculation....', LogLevel.Info)
    for time_frame in time_frames:
        cal_baseline_mean = mean_calculation.calculate_norm_mean(stimulation_time_frame,
                                                                 time_frame)

        write_message(
            'Baseline Mean Calculation of Cell {0} finished: -> Baseline Mean {1}'.format(time_frame[0],
                                                                                          cal_baseline_mean),
            LogLevel.Verbose)
        cell_data.append(Cell.Cell(time_frame[0], cal_baseline_mean, 0, 0, 0, 0, 0, 0, 0))
    write_message('Baseline Mean Calculation done', LogLevel.Info)


def calculate_mean(normalised_cells):
    """
    Calculate the mean. Normalised Cells will be provided
    :param normalised_cells:
    :return:
    """
    write_message('Starting Mean Calculation...', LogLevel.Info)
    index = 0
    for normalised_cell in normalised_cells:
        mean = mean_calculation.calculate_mean(normalised_cell[1:])
        cell_data[index].mean = mean
        index += 1
    write_message('Mean Calculation done', LogLevel.Info)


def maximum_detection(normalised_cells):
    """
    Calculate the Maximum from given Data Set.
    :param normalised_cells:
    :return:
    """
    write_message('Detecting Maximum ....', LogLevel.Info)
    index = 0
    for normalised_cell in normalised_cells:
        cell_max = min_max.calculate_maximum(normalised_cell[1:])
        cell_data[index].maximum = cell_max
        index += 1
    write_message('Maximum Detection done', LogLevel.Info)


def calculate_limit():
    """
    Calculate Limit for each Cell
    :return:
    """
    write_message('Calculating Limit...', LogLevel.Info)
    index = 0
    for cell in cell_data:
        sixty_percent_of_maximum = min_max.calculate_limit_from_maximum(cell.maximum)
        cell_data[index].limit = sixty_percent_of_maximum
        index += 1
    write_message('Calculating Limit done', LogLevel.Info)


def over_under_limit(normalised_cells):
    """
    Check if a data entry of a given cell is over or under the cells limit
    :param normalised_cells:
    :return:
    """
    write_message('Calculating Over and Under Limit...', LogLevel.Info)
    index = 0
    over_under_limit_raw_data = min_max.calculate_over_and_under(normalised_cells, cell_data)
    for over_under_cell_data in over_under_limit_raw_data:
        cell_data[index].over_under_limit = over_under_cell_data[1:]
        index += 1
    write_message('Calculating Over and Under Limit done', LogLevel.Info)


def calculate_high_stimulus_per_minute(row_count):
    """
    Calculates high stimulus frames per cell
    :param row_count:
    :return:
    """
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
