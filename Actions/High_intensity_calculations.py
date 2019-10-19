import datetime
from Services.Logger import Log
from UI import Questions
from GlobalData import Statics
from Services.Config import Config

'''
Main Calculation Function
'''


def start_high_intensity_calculations():
    """
    High Intensity Calculations done here.
    :return:
    """

    Statics.reset_input_and_output()
    Questions.ask_files_to_process()

    for input_file in Statics.input_files:
        input_file.get_folder()
        input_file.get_file_name()
        input_file.read_time_traces_file()
        input_file.create_cells()
        input_file.calculate_minutes()

    Questions.ask_stimulation_time_frames()
    Questions.ask_percentage_limit()
    Questions.ask_file_output()
    Questions.conclusion()

    for input_file in Statics.input_files:
        print()
        Log.write_message('Processing file {0}'.format(input_file.name), Log.LogLevel.Info)
        execute_high_intensity_calculation(input_file)

    return True


def execute_high_intensity_calculation(file):
    start_time = datetime.datetime.now()
    file.calculate_baseline_mean()
    if Config.Config.NORMALIZATION_METHOD == Statics.NormalizationMethods.Baseline:
        file.normalize_timeframes_with_baseline()
    else:
        file.normalize_timeframes_with_to_ones()
    
    file.calculate_timeframe_maximum()
    file.calculate_threshold()
    file.detect_above_threshold()
    file.count_high_intensity_peaks_per_minute()
    file.calculate_spikes_per_min_per_cell()
    for output_option in Statics.selected_output_options:
        if output_option == Statics.OutputOptions.High_Stimulus.value:
            file.write_high_intensity_counts()
        elif output_option == Statics.OutputOptions.Normalized_Data.value:
            file.write_normalized_timeframes()
        elif output_option == Statics.OutputOptions.Spikes_Per_Minute.value:
            file.write_spikes_per_minute()
    end_time = datetime.datetime.now()
    Log.write_message('Calculation done in {0} seconds.'.format(end_time - start_time), Log.LogLevel.Verbose)
    Log.write_message('{0} Timeframes processed'.format(len(file.cells) * len(file.cells[0].timeframes)),
                      Log.LogLevel.Verbose)
