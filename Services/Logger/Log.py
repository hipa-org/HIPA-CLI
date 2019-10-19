from Services.Config.Config import Config
from enum import Enum
import datetime
from clint.textui import puts, colored


class LogLevel(Enum):
    def __str__(self):
        return str(self.value)

    Verbose = 0
    Info = 1
    Debug = 2
    Warn = 3
    Error = 4


def write_message(message, log_level):
    """
    Writes a log message. Logger behaves on specific cli arguments like debug or verbose mode
    :param message:
    :param log_level:
    :return:
    """
    if log_level == LogLevel.Error or log_level == LogLevel.Warn:
        write_error_log(message)
    else:
        write_default_log(message)

    if Config.VERBOSE == 1 and Config.DEBUG == 1:
        if log_level == LogLevel.Verbose:
            puts(colored.cyan('Verbose: {0}'.format(message)))
        elif log_level == LogLevel.Info:
            puts(colored.green('Info: {0}'.format(message)))
        elif log_level == LogLevel.Debug:
            puts(colored.white('Debug: {0}'.format(message)))
        elif log_level == LogLevel.Warn:
            puts(colored.yellow('Warn: {0}'.format(message)))
        elif log_level == LogLevel.Error:
            puts(colored.red('Error: {0}'.format(message)))

    elif Config.VERBOSE == 1 and Config.DEBUG == 0:
        if log_level == LogLevel.Verbose:
            puts(colored.cyan('Verbose: {0}'.format(message)))

        elif log_level == LogLevel.Info:
            puts(colored.green('Info: {0}'.format(message)))
        elif log_level == LogLevel.Warn:
            puts(colored.yellow('Warn: {0}'.format(message)))
        elif log_level == LogLevel.Error:
            puts(colored.red('Error: {0}'.format(message)))

    elif Config.DEBUG == 1 and Config.VERBOSE == 0:
        if log_level == LogLevel.Info:
            puts(colored.green('Info: {0}'.format(message)))
        elif log_level == LogLevel.Debug:
            puts(colored.white('Debug: {0}'.format(message)))
        elif log_level == LogLevel.Warn:
            puts(colored.yellow('Warn: {0}'.format(message)))
        elif log_level == LogLevel.Error:
            puts(colored.red('Error: {0}'.format(message)))

    elif Config.DEBUG == 0 and Config.VERBOSE == 0:
        if log_level == LogLevel.Info:
            puts(colored.green('Info: {0}'.format(message)))
        elif log_level == LogLevel.Warn:
            puts(colored.yellow('Warn: {0}'.format(message)))
        elif log_level == LogLevel.Error:
            puts(colored.red('Error: {0}'.format(message)))


def write_default_log(message):
    """
    Writes a default log message when no cli argument is given
    :param message:
    :return:
    """
    now = datetime.datetime.now()
    fh = open('{0}{1}'.format(Config.LOG_DIRECTORY, Config.DEFAULT_LOG), "a")
    fh.write('{0}: {1}\n'.format(str(now), message))
    fh.close()


def write_error_log(message):
    """
    Writes an error message
    :param message:
    :return:
    """
    now = datetime.datetime.now()
    fh = open('{0}{1}'.format(Config.LOG_DIRECTORY, Config.ERROR_LOG), "a")
    fh.write('{0}: {1}\n'.format(str(now), message))
    fh.close()


