from pathlib import Path
from Shared.Services.Configuration.Parser.Argument_Parser import CLIArguments
import logging
import sys


class CliConfiguration:
    class GeneralConfig:
        DEBUG = False
        START_HIGH_INTENSITY_CALCULATION = False

    class DataConfig:
        # Folder
        WORKING_DIRECTORY = 'Data/'

        # File names
        OUTPUT_FILE_NAME_HIGH_STIMULUS = 'High-Stimulus'
        OUTPUT_FILE_NAME_NORMALIZED_DATA = 'Normalized-Data'
        OUTPUT_FILE_NAME_SPIKES_PER_MINUTE = 'Spikes_Per_Minute'

        # Data
        DATA_ROOT_DIRECTORY = Path()
        DATA_RAW_DIRECTORY = Path()
        DATA_RESULTS_DIRECTORY = Path()


def load_cli_config(config):
    __load_general_config(config['general'])
    __load_data_config(config['data'])


def __load_data_config(data_config):
    try:

        # Directories
        CliConfiguration.DataConfig.DATA_ROOT_DIRECTORY = Path(data_config['ROOT_DIRECTORY'])
        CliConfiguration.DataConfig.DATA_RAW_DIRECTORY = Path(CliConfiguration.DataConfig.DATA_ROOT_DIRECTORY,
                                                              data_config['RAW_DIRECTORY'])
        CliConfiguration.DataConfig.DATA_RESULTS_DIRECTORY = Path(CliConfiguration.DataConfig.DATA_ROOT_DIRECTORY,
                                                                  data_config['RESULTS_DIRECTORY'])

        # File Names
        CliConfiguration.DataConfig.OUTPUT_FILE_NAME_HIGH_STIMULUS = data_config[
            'OUTPUT_FILE_NAME_HIGH_STIMULUS']
        CliConfiguration.DataConfig.OUTPUT_FILE_NAME_NORMALIZED_DATA = data_config[
            'OUTPUT_FILE_NAME_NORMALIZED_DATA']
        # CliConfiguration.DataConfig.NORMALIZATION_METHOD = data_config['normalization_method']

    except KeyError as ex:
        logging.error(f"Error occurred while reading config.ini.")
        logging.error(f"Key: {ex} not found!")
        logging.error(f"Make sure the file config.ini exists in your src directory!")
        sys.exit()


def __load_general_config(general_config):
    try:
        CliConfiguration.GeneralConfig.DEBUG = general_config.getboolean('DEBUG_MODE', False)

        if CLIArguments.debug:
            CliConfiguration.GeneralConfig.DEBUG = True
            logging.debug('IMPORTANT NOTICE: DEBUG MODE IS ACTIVE!')

        if CLIArguments.start_high_intensity_calculations:
            CliConfiguration.GeneralConfig.START_HIGH_INTENSITY_CALCULATION = True

    except KeyError as ex:
        logging.error(f"Error occurred while reading config.ini.")
        logging.error(f"Key: {ex} not found!")
        logging.error(f"Make sure the file config.ini exists in your src directory!")
        sys.exit()
