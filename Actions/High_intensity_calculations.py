from Classes.Cell import create_cells
import datetime
from Services.Logger import Log
from Services.Filemanagement import Read, Write
from Services import Calculations
from UI import Console, Questions
from GlobalData import Statics

'''
Main Calculation Function
'''


def start_high_intensity_calculations():
    Statics.reset_input_and_output()

    Questions.ask_files_to_process()
    Read.read_time_traces_file()
    for file in Statics.input_files:
        create_cells(file)
        Calculations.DataSizes.calculate_minutes(file)

    Questions.ask_stimulation_time_frame()
    Questions.ask_percentage_limit()
    Questions.ask_file_output()
    Questions.conclusion()

    for file in Statics.input_files:
        Log.write_message('Processing file {0}'.format(file.name), Log.LogLevel.Info)
        execute_high_intensity_calculation(file)

    return True


def execute_high_intensity_calculation(file):
    start_time = datetime.datetime.now()
    Calculations.Mean.calculate_baseline_mean(file)
    Calculations.Normalization.normalize_timeframes(file)
    Calculations.Min_max.calculate_timeframe_maximum(file)
    Calculations.Min_max.calculate_threshold(file)
    Calculations.HighIntensity.detect_above_threshold(file)
    Calculations.HighIntensity.count_high_intensity_peaks_per_minute(file)
    for output_option in Statics.selected_output_options:
        if output_option == Statics.OutputOptions.High_Stimulus.value:
            Write.high_stimulus_counts(file)
        elif output_option == Statics.OutputOptions.Normalized_Data.value:
            Write.normalized_timeframes(file)
    end_time = datetime.datetime.now()
    Log.write_message('Calculation done in {0} seconds.'.format(end_time - start_time), Log.LogLevel.Verbose)
    Log.write_message('{0} Timeframes processed'.format(len(file.cells) * len(file.cells[0].timeframes)),
                      Log.LogLevel.Verbose)
