import configparser
import sys
import logging
from pathlib import Path
from Shared.Services.Config.ArgumentParser import CLIArguments
from Shared.Database import Database_Configuration

# Configuration.py
class Config:
    VERBOSE = False
    DEBUG = False

    # Web Server
    START_WEB_SERVER = False

    # Folder
    WORKING_DIRECTORY = 'Data/'

    # File names
    OUTPUT_FILE_NAME_HIGH_STIMULUS = 'High-Stimulus'
    OUTPUT_FILE_NAME_NORMALIZED_DATA = 'Normalized-Data'
    OUTPUT_FILE_NAME_SPIKES_PER_MINUTE = 'Spikes_Per_Minute'
    NORMALIZATION_METHOD = 'Baseline'

    START_HIGH_INTENSITY_CALCULATION = False

    # Data
    DATA_ROOT_DIRECTORY = Path()
    DATA_RAW_DIRECTORY = Path()
    DATA_RESULTS_DIRECTORY = Path()


class HTTPServerConfig:
    pass


def load_configuration():
    """
    Loads the Config.ini File, and stores the values into the Config Class
    :return:
    """
    config = configparser.ConfigParser()

    # Load the web server config, otherwise load cli config
    if CLIArguments.start_web_server is not None:
        config.read('Config/web-config.ini')

    else:
        config.read('Config/config.ini')



    try:
        print(config['mysql'])
        Database_Configuration.load_database_config(config['mysql'])
        Config.OUTPUT_FILE_NAME_HIGH_STIMULUS = config['FILES']['output_file_name_high_stimulus']
        Config.OUTPUT_FILE_NAME_NORMALIZED_DATA = config['FILES']['output_file_name_normalized_data']
        Config.NORMALIZATION_METHOD = config['FILES']['normalization_method']

        # Data
        Config.DATA_ROOT_DIRECTORY = Path(config['DATA']['root_directory'])
        Config.DATA_RAW_DIRECTORY = Path(Config.DATA_ROOT_DIRECTORY, config['DATA']['raw_directory'])
        Config.DATA_RESULTS_DIRECTORY = Path(Config.DATA_ROOT_DIRECTORY, config['DATA']['results_directory'])
        return
    except KeyError as ex:
        logging.error(f"Error occurred while reading config.ini.")
        logging.error(f"Key: {ex} not found!")
        logging.error(f"Make sure the file config.ini exists in your src directory!")
        sys.exit()




def reset_config():
    """
    Resets the Config File. In fact the Config.ini file will be rewritten in total.
    :return:
    """
    config = configparser.ConfigParser()
    config['SETTINGS'] = {
        'input_file_name': 'time_traces',
        'working_directory': 'Data/',
        'output_file_name_high_stimulus': 'High-Stimulus',
        'output_file_name_normalized_data': 'Normalized-Data',
        'normalization_method': 'Baseline'
    }
    config['LOGS'] = {
        'logs_path': 'Logs/',
        'error_log': 'error-log.txt',
        'default_log': 'default-log.txt'
    }
    with open('Config.ini', 'w') as configfile:
        try:
            config.write(configfile)
            configfile.close()
            return True
        except FileNotFoundError as ex:
            return ex
