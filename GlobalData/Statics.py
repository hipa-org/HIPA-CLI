from enum import Enum

input_files = []
selected_output_options = []


class OutputOptions(Enum):
    High_Stimulus = 'High Stimulus'
    Normalized_Data = 'Normalized Data'


def init():
    global input_files
    global selected_output_options
    input_files = []
    selected_output_options = []


def reset_input_and_output():
    global input_files
    global selected_output_options
    input_files = []
    selected_output_options = []
