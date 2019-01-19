import configparser


# Config.py
class Config:
    VERBOSE = 0
    DEBUG = 0
    WORKING_DIRECTORY = 'Data/'
    INPUT_FILE_NAME = 'time_traces'
    OUTPUT_FILE_NAME_HIGH_STIMULUS = 'High-Stimulus'
    OUTPUT_FILE_NAME_NORMALIZED_DATA = 'Normalized-Data'
    ERROR_LOG = 'error-log.txt'
    DEFAULT_LOG = 'default-log.txt'
    LOG_DIRECTORY = 'Logs/'


def read_conf():
    """
    Reads the Config.ini File, and stores the values into the Config Class
    :return:
    """
    config = configparser.ConfigParser()
    config.read('Config.ini')
    try:
        Config.OUTPUT_FILE_NAME_HIGH_STIMULUS = config['SETTINGS']['output_file_name_high_stimulus']
        Config.OUTPUT_FILE_NAME_NORMALIZED_DATA = config['SETTINGS']['output_file_name_normalized_data']
        Config.INPUT_FILE_NAME = config['SETTINGS']['input_file_name']
        Config.WORKING_DIRECTORY = config['SETTINGS']['working_directory']
        Config.DEFAULT_LOG = config['LOGS']['default_log']
        Config.ERROR_LOG = config['LOGS']['error_log']
        Config.LOG_DIRECTORY = config['LOGS']['logs_path']
        return True
    except KeyError as ex:
        return ex


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
        'output_file_name_normalized_data': 'Normalized-Data'
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
