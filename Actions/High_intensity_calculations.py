from Classes.Cell import Cell, create_cells
import datetime
from Services.Logger.log import write_message, LogLevel
from Services.Filemanagement.read_files import read_time_traces_file
from Services.Filemanagement.write_files import write_high_stimulus_file, write_normalized_data
from Services.Calculations import normalisation, mean, min_max, high_intensity, DataSizes

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
    start_time = datetime.datetime.now()
    mean.calculate_baseline_mean(file)
    normalisation.normalise_timeframes(file)
    min_max.calculate_timeframe_maximum(file)
    min_max.calculate_threshold(file)
    high_intensity.detect_above_below_threshold(file)
    high_intensity.collect_all_high_stimulus(file)
    end_time = datetime.datetime.now()
    write_message('Calculation done in {0} seconds.'.format(end_time - start_time), LogLevel.Verbose)
    write_message('{0} data points processed'.format(len(file.cells) * len(file.cells[0].timeframes)), LogLevel.Verbose)

''' 
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

'''





