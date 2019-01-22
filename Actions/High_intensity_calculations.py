from Classes.Cell import create_cells
import datetime
from Services.Logger import Log
from Services.Filemanagement import Read, Write
from Services import Calculations
from UI import Console, Questions
from GlobalData.Statics import input_files, selected_output_options, reset_input_and_output, OutputOptions

'''
Main Calculation Function
'''


def start_high_intensity_calculations():
    reset_input_and_output()

    Questions.ask_files_to_process()
    Read.read_time_traces_file()
    for file in input_files:
        create_cells(file)
        Calculations.DataSizes.calculate_minutes(file)

    Questions.ask_stimulation_time_frame()
    Questions.ask_percentage_limit()
    Questions.ask_file_output()
    conclusion()

    for file in input_files:
        Log.write_message('Processing file {0}'.format(file.name), Log.LogLevel.Info)
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
    Console.print_hic_headline()
    Log.write_message("You selected the following output options:", Log.LogLevel.Info)
    for output in selected_output_options:
        Log.write_message(output, Log.LogLevel.Info)

    print()
    for file in input_files:
        Log.write_message(
            'You are processing the File {0} with following arguments: \nStimulation Timeframe: {1}\nPercentage: {2}'.format(
                file.name, file.stimulation_timeframe, file.percentage_limit), Log.LogLevel.Info)
        print()

    input("Press any Key to start Calculations.")


def execute_high_intensity_calculation(file):
    start_time = datetime.datetime.now()
    Calculations.Mean.calculate_baseline_mean(file)
    Calculations.Normalization.normalize_timeframes(file)
    Calculations.Min_max.calculate_timeframe_maximum(file)
    Calculations.Min_max.calculate_threshold(file)
    Calculations.HighIntensity.detect_above_threshold(file)
    Calculations.HighIntensity.count_high_intensity_peaks_per_minute(file)
    for output_option in selected_output_options:
        if output_option == OutputOptions.High_Stimulus.value:
            Write.high_stimulus_file(file)
       # elif output_option == OutputOptions.Normalized_Data.value:
           # Write.write_normalized_data(cell_data, file_name)
    end_time = datetime.datetime.now()
    Log.write_message('Calculation done in {0} seconds.'.format(end_time - start_time), Log.LogLevel.Verbose)
    Log.write_message('{0} Timeframes processed'.format(len(file.cells) * len(file.cells[0].timeframes)),
                      Log.LogLevel.Verbose)


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
