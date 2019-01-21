import os
from Services.Config.Config import Config


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


def create_needed_files():
    dir_exist = os.path.exists(Config.LOG_DIRECTORY)
    if dir_exist is not True:
        create_logs_dir()

    log_file_exists = os.path.exists('{0}{1}'.format(Config.LOG_DIRECTORY, Config.DEFAULT_LOG))
    if log_file_exists is not True:
        create_default_log_file()

    log_file_exists = os.path.exists('{0}{1}'.format(Config.LOG_DIRECTORY, Config.ERROR_LOG))
    if log_file_exists is not True:
        create_error_log_file()
