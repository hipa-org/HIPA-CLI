import datetime
from UI import Questions
from RuntimeConstants import Runtime_Datasets
from Classes.File import File
import logging

'''
Main Calculation Function
'''


def start_high_intensity_calculations():
    """
    High Intensity Calculations done here.
    :return:
    """

    Questions.ask_stimulation_time_frames()
    Questions.ask_threshold()
    Questions.conclusion()

    for input_file in Runtime_Datasets.Files:
        print()
        logging.info(f'Processing file {input_file.name}')
        execute_high_intensity_calculation(input_file)

    return True


def execute_high_intensity_calculation(file: File):
    start_time = datetime.datetime.now()
    file.calculate_baseline_mean()
    file.normalize_time_frames_with_to_ones()
    file.calculate_time_frame_maximum()
    file.calculate_threshold()
    file.detect_above_threshold()
    file.count_high_intensity_peaks_per_minute()
    file.summarize_high_intensity_peaks()
    file.split_cells()
    file.calculate_high_stimulus_count_per_interval()
    file.generate_report()

    end_time = datetime.datetime.now()
    logging.info(f'Evaluation of file {file.name} done.')
    logging.info(f'Calculation done in {end_time - start_time} seconds.')
    logging.info(f'{len(file.cells) * len(file.cells[0].time_frames)} time frames processed')
    input()
