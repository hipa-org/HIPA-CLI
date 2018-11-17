import configparser


# config.py
class Config:
    VERBOSE = 0
    DEBUG = 0
    WORKING_DIRECTORY = 'Data/'
    INPUT_FILE_NAME = 'time_traces'
    OUTPUT_FILE_NAME = 'Result'
    ERROR_LOG = 'error-log.txt'
    DEFAULT_LOG = 'default-log.txt'
    LOG_DIRECTORY = 'Logs/'


def read_conf():
    config = configparser.ConfigParser()
    config.read('config.ini')
    try:
        Config.OUTPUT_FILE_NAME = config['SETTINGS']['output_file_name']
        Config.INPUT_FILE_NAME = config['SETTINGS']['input_file_name']
        Config.WORKING_DIRECTORY = config['SETTINGS']['working_directory']
        Config.DEFAULT_LOG = config['LOGS']['default_log']
        Config.ERROR_LOG = config['LOGS']['error_log']
        Config.LOG_DIRECTORY = config['LOGS']['logs_path']
        return True
    except KeyError as ex:
        return ex


def reset_config():
    config = configparser.ConfigParser()
    config['SETTINGS'] = {
        'input_file_name': 'time_traces',
        'working_directory': 'Data/',
        'output_file_name': 'Result',
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
