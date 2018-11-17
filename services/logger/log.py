from services.config.config import Config
from enum import Enum
from services.files.create_files import create_log_file
import os
import datetime
from clint.textui import puts, colored, indent


class LogLevel(Enum):
    Verbose = 0
    Info = 1
    Debug = 2
    Warn = 3
    Error = 4


def write_message(message, log_level):
    write_log(message)
    if Config.VERBOSE == 1 and Config.VERBOSE == 1:
        if log_level == LogLevel.Verbose:
            puts(colored.blue('Verbose: {0}'.format(message)))
        elif log_level == LogLevel.Info:
            puts(colored.green('Info: {0}'.format(message)))
        elif log_level == LogLevel.Debug:
            puts(colored.white('Debug: {0}'.format(message)))
        elif log_level == LogLevel.Warn:
            puts(colored.yellow('Warn: {0}'.format(message)))
        elif log_level == LogLevel.Error:
            puts(colored.red('Error: {0}'.format(message)))

    elif Config.VERBOSE == 1:
        if log_level == LogLevel.Verbose:
            puts(colored.blue('Verbose: {0}'.format(message)))
        elif log_level == LogLevel.Info:
            puts(colored.green('Info: {0}'.format(message)))
        elif log_level == LogLevel.Warn:
            puts(colored.yellow('Warn: {0}'.format(message)))
        elif log_level == LogLevel.Error:
            puts(colored.red('Error: {0}'.format(message)))

    elif Config.DEBUG == 1:
        if log_level == LogLevel.Verbose:
            puts(colored.blue('Verbose: {0}'.format(message)))
        elif log_level == LogLevel.Info:
            puts(colored.green('Info: {0}'.format(message)))
        elif log_level == LogLevel.Debug:
            puts(colored.white('Debug: {0}'.format(message)))
        elif log_level == LogLevel.Warn:
            puts(colored.yellow('Warn: {0}'.format(message)))
        elif log_level == LogLevel.Error:
            puts(colored.red('Error: {0}'.format(message)))

    else:
        if log_level == LogLevel.Info:
            puts(colored.green('Info: {0}'.format(message)))
        elif log_level == LogLevel.Debug:
            puts(colored.white('Debug: {0}'.format(message)))
        elif log_level == LogLevel.Warn:
            puts(colored.yellow('Warn: {0}'.format(message)))
        elif log_level == LogLevel.Error:
            puts(colored.red('Error: {0}'.format(message)))


def write_log(message):
    file_exists = os.path.exists("Log/")
    now = datetime.datetime.now()
    if not file_exists:
        create_log_file()

    fh = open("Log/log.txt", "a")
    fh.write('{0}: {1}\n'.format(str(now), message))
    fh.close()
