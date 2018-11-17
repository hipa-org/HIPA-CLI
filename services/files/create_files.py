import os
from services.config.config import Config


def create_logs_dir():
    os.makedirs(Config.LOG_DIRECTORY)


def create_default_log_file():
    log_file = open('{0}{1}'.format(Config.LOG_DIRECTORY, Config.DEFAULT_LOG), "w")
    log_file.write('Created Log\n')
    log_file.close()


def create_error_log_file():
    log_file = open('{0}{1}'.format(Config.LOG_DIRECTORY, Config.ERROR_LOG), "w")
    log_file.write('Created Log\n')
    log_file.close()
