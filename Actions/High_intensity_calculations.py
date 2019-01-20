from Classes.Cell import Cell, create_cells
import datetime
from Services.Logger.log import write_message, LogLevel
from Services.Filemanagement.read_files import read_time_traces_file
from Services.Filemanagement.write_files import write_high_stimulus_file, write_normalized_data
from Services.Calculations import normalisation, mean_calculation, min_max, high_stimulus, DataSizes

from UI.UI import print_empty_line, print_hic_headline
from UI.Questions import ask_files_to_process, ask_stimulation_time_frame, ask_file_output, ask_percentage_limit
from GlobalData.Statics import input_files, selected_output_options, reset_input_and_output





'''
Main Calculation Function
'''


def start_high_intensity_calculations():
    reset_input_and_output()

    ask_files_to_process()
    read_time_traces_file()
    for file in input_files:
        create_cells(file)
        DataSizes.calculate_minutes(file)

    ask_stimulation_time_frame()
    ask_percentage_limit()
    ask_file_output()
    conclusion()

    for file in input_files:
        write_message('Processing file {0}'.format(file.name), LogLevel.Info)
        execute_high_intensity_calculation(file)

    return True
'''
 detectDataSizes.detect_row_and_column_count(file)
 ask_stimulation_time_frame()

 time_frames = create_time_frame_array(time_traces)
 data_count = detectDataSizes.detect_row_and_column_count(time_frames)

 ask_percentage()
 ask_file_output()
 conclusion()
 for file in input_files:
     time_traces = read_time_traces_file(file.name)

     cell_data = []
     print_empty_line()
     write_message('Processing file {0}'.format(file.name), LogLevel.Info)
     execute_high_intensity_calculation(file.name, file.stimulation_time_frame)
 '''


'''
Resets the previous Input
'''



'''
Prints a conclusion before starting the Calculations
'''


def conclusion():
    print_hic_headline()
    write_message("You selected the following output options:", LogLevel.Info)
    for output in selected_output_options:
        write_message(output, LogLevel.Info)

    print()
    for file in input_files:
        write_message(
            'You are processing the File {0} with following arguments: \nStimulation Timeframe: {1}\nPercentage: {2}'.format(
                file.name, file.stimulation_timeframe, file.percentage_limit), LogLevel.Info)
        print()

    input("Press any Key to start Calculations.")


def execute_high_intensity_calculation(file):

    baseline_mean_calculation(file)


   ''' start_time = datetime.datetime.now()
    time_traces = read_time_traces_file(file_name)
    time_frames = create_time_frame_array(time_traces)
    data_count = calculate_provided_data(time_frames)
    baseline_mean_calculation(time_frames, stimulation_time_frame)
    normalized_cells = normalize_cells(time_frames)
    calculate_mean(normalized_cells)
    maximum_detection(normalized_cells)
    calculate_limit(file_name)
    over_under_limit(normalized_cells)
    calculate_high_stimulus_per_minute(data_count[1])
    for output_option in selected_output_options:
        if output_option == OutputOptions.High_Stimulus.value:
            write_high_stimulus_file(cell_data, file_name)
        elif output_option == OutputOptions.Normalized_Data.value:
            write_normalized_data(cell_data, file_name)

    end_time = datetime.datetime.now()
    write_message('Calculation done in {0} seconds.'.format(end_time - start_time), LogLevel.Verbose)
    write_message('{0} data points processed'.format(data_count[0] * data_count[1]), LogLevel.Verbose)
    '''


'''
Normalize Cells
'''


def normalize_cells(time_frames):
    write_message('Starting Cell Normalization....', LogLevel.Info)
    normalized_data_cells = normalisation.normalise_columns(cell_data, time_frames)
    index = 0
    for normalized_data in normalized_data_cells:
        cell_data[index].normalized_data = normalized_data[1:]
        index += 1
    write_message('Cell Normalization Done....', LogLevel.Info)
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
    data_count = DataSizes.detect_row_and_column_count(time_frames)
    minutes = DataSizes.calculate_minutes(data_count[1])
    write_message('Detected {0} Columns including Avg and Err'.format(data_count[0]), LogLevel.Info)
    write_message('Detected {0} Rows excluding the Header Row'.format(data_count[1]), LogLevel.Info)
    write_message('Detected {0} Minutes '.format(minutes), LogLevel.Info)
    return data_count


'''
Mean of Intensities before Stimulation
'''


def baseline_mean_calculation(time_frames, stimulation_time_frame):
    global cell_data
    write_message('Starting Baseline Mean Calculation....', LogLevel.Info)
    for time_frame in time_frames:
        cal_baseline_mean = mean_calculation.calculate_norm_mean(stimulation_time_frame,
                                                                 time_frame)
        write_message(
            'Baseline Mean Calculation of Cell {0} finished: -> Baseline Mean {1}'.format(time_frame[0],
                                                                                          cal_baseline_mean),
            LogLevel.Verbose)
        cell_data.append(Cell.Cell(time_frame[0], time_frame, cal_baseline_mean, 0, 0, 0, 0, 0, 0))
    write_message('Baseline Mean Calculation done', LogLevel.Info)


'''
Calculate the mean. Normalised Cells will be provided
'''


def calculate_mean(normalised_cells):
    global cell_data
    write_message('Starting Mean Calculation...', LogLevel.Info)
    index = 0
    for normalised_cell in normalised_cells:
        mean = mean_calculation.calculate_mean(normalised_cell[1:])
        write_message('Calculated Mean -> {0}'.format(mean), LogLevel.Verbose)
        cell_data[index].mean = mean
        index += 1
    write_message('Mean Calculation done', LogLevel.Info)


'''
Calculate the Maximum from given Data Set. 
'''


def maximum_detection(normalised_cells):
    global cell_data
    write_message('Detecting Maximum ....', LogLevel.Info)
    index = 0
    for normalised_cell in normalised_cells:
        cell_max = min_max.calculate_maximum(normalised_cell[1:])
        write_message('Maximum of cell {0}-> {1}'.format(cell_data[index], cell_max), LogLevel.Verbose)
        cell_data[index].maximum = cell_max
        index += 1

    write_message('Maximum Detection done', LogLevel.Info)


'''
Calculate Limit for each Cell
'''


def calculate_limit(file_name):
    global selected_files_to_process
    global cell_data
    write_message('Calculating Threshold...', LogLevel.Info)

    for file in selected_files_to_process:
        if file.name == file_name:
            index = 0
            for cell in cell_data:
                cell_data[index].limit = min_max.calculate_limit_from_maximum(cell.maximum, file.percentage)
                write_message(
                    'Threshold -> {0}'.format(min_max.calculate_limit_from_maximum(cell.maximum, file.percentage)),
                    LogLevel.Verbose)
                index += 1
    write_message('Calculating Threshold done', LogLevel.Info)


'''
Check if a data entry of a given cell is over or under the cells limit
'''


def over_under_limit(normalised_cells):
    global cell_data
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
    global cell_data
    write_message('Calculating High Stimulus per Minute per Cell...', LogLevel.Info)
    temp_over_under_limit = []
    for cell in cell_data:
        temp_over_under_limit.append(cell.over_under_limit)

    high_stimulus_per_minute = high_stimulus.calculate_high_stimulus_per_minute(
        temp_over_under_limit, row_count)
    index = 0
    for high_stimulus_per_cell in high_stimulus_per_minute:
        # print(high_stimulus_per_cell)
        cell_data[index].high_stimulus_per_minute = high_stimulus_per_cell
        index += 1
    write_message('Calculation High Stimulus per Minute per Cell done', LogLevel.Info)
