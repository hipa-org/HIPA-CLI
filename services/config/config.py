import configparser


# config.py
class Config:
    VERBOSE = 0
    DEBUG = 0
    DEFAULT_WORKING_DIRECTORY = 'Data/'
    DEFAULT_INPUT_FILE_NAME = 'time_traces'
    DEFAULT_OUTPUT_FILE_NAME = 'Results'
    ERROR_LOG = 'error-log.txt'
    DEFAULT_LOG = 'default-log.txt'
    LOG_DIRECTORY = 'Logs/'


def read_conf():
    config = configparser.ConfigParser()
    config.read('config.ini')
    try:
        Config.DEFAULT_OUTPUT_FILE_NAME = config['SETTINGS']['default_output_file_name']
        Config.DEFAULT_INPUT_FILE_NAME = config['SETTINGS']['default_input_file_name']
        Config.DEFAULT_WORKING_DIRECTORY = config['SETTINGS']['default_working_directory']
        Config.DEFAULT_LOG = config['LOGS']['default_log']
        Config.ERROR_LOG = config['LOGS']['error_log']
        Config.LOG_DIRECTORY = config['LOGS']['logs_path']
        return True
    except KeyError as ex:
        return ex


def reset_config():
    config = configparser.ConfigParser()
    config['SETTINGS'] = {
        'default_input_file_name': 'time_traces',
        'default_working_directory': 'Data/',
        'default_output_file_name': 'Results'
    }
    config['LOGS'] = {
        'logs_path': 'Logs/',
        'error_log': 'error-log.txt',
        'default_log': 'default-log.txt'
    }
    with open('config.ini', 'w') as configfile:
        try:
            config.write(configfile)
            configfile.close()
            return True
        except FileNotFoundError as ex:
            return ex
