from services.config.config import Config
from enum import Enum
from services.files.create_files import create_log_file
import os
import datetime


class LogLevel(Enum):
    Verbose = 0
    Info = 1
    Debug = 2
    Warn = 3
    Error = 4


def write_message(message, log_level):
    write_log(message)
    if Config.VERBOSE == 1:
        if log_level == LogLevel.Verbose:
            print('Verbose: {0}'.format(message))
        elif log_level == LogLevel.Info:
            print('Info: {0}'.format(message))
        elif log_level == LogLevel.Debug:
            print('Info: {0}'.format(message))
        elif log_level == LogLevel.Warn:
            print('Warn: {0}'.format(message))
        elif log_level == LogLevel.Error:
            print('Error: {0}'.format(message))
    else:
        if log_level == LogLevel.Info:
            print('Info: {0}'.format(message))
        elif log_level == LogLevel.Debug:
            print('Info: {0}'.format(message))
        elif log_level == LogLevel.Warn:
            print('Warn: {0}'.format(message))
        elif log_level == LogLevel.Error:
            print('Error: {0}'.format(message))


def write_log(message):
    file_exists = os.path.exists("Log/log.txt")
    now = datetime.datetime.now()
    if not file_exists:
        create_log_file()

    fh = open("Log/log.txt", "a")
    fh.write('{0}: {1}\n'.format(str(now), message))
    fh.close()
