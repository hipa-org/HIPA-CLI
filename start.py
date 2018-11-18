import sys
import argparse
from pyfiglet import Figlet
import inquirer
from enum import Enum
from actions import high_intensity_calculations
from services.config.config import Config, read_conf, reset_config
import os
from services.logger.log import write_message, LogLevel
from services.filemanagement.write_files import write_high_stimulus_file
from services.filemanagement.create_files import create_needed_files
import webbrowser


class Actions(Enum):
    HIGH_INTENSITY_PEAK_ANALYSIS = 'High Intensity Peak Analysis'
    CELL_SORTER = 'Cell Sorter'
    HELP = 'Help'


class DebugActions(Enum):
    FILESYSTEM_TEST = 'File System Test'


def start():
    ap = argparse.ArgumentParser()
    ap.add_argument("-V", "--verbose", required=False,
                    action='store_true',
                    help="Activate verbose Output")
    ap.add_argument("-H", "--highintense", required=False,
                    action='store_true',
                    help='Direct call of calculation')
    ap.add_argument("-d", "--debug", required=False,
                    action='store_true',
                    help="Starts the program in Debug Mode")
    ap.add_argument("-r", "--restore", required=False,
                    action='store_true',
                    help="Restores the default config.ini")

    args = vars(ap.parse_args())
    create_needed_files()
    handle_args(args)
    success = read_conf()
    if success is not True:
        write_message('Error reading {0} from config.ini. Please check your config file'.format(success),
                      LogLevel.Error)
    start_up_actions()


def handle_args(arguments):
    if arguments['verbose']:
        Config.VERBOSE = 1

    if arguments['highintense']:
        high_intensity_calculations.start_high_intensity_calculations()
        sys.exit(21)

    if arguments['debug']:
        Config.DEBUG = 1
        write_message('IMPORTANT NOTICE: DEBUG MODE IS ACTIVE!', LogLevel.Info)

    if arguments['restore']:
        success = reset_config()
        if success is not True:
            write_message(success, LogLevel.Error)
        else:
            write_message('Restored Config.ini', LogLevel.Info)

    write_message('Arguments {0}'.format(arguments), LogLevel.Verbose)


def start_up_actions():
    clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
    clear()
    f = Figlet(font='slant')
    print(f.renderText('Intensity Analyzer'))
    if Config.DEBUG == 1:
        questions = [
            inquirer.List('action',
                          message="Choose Action?",
                          choices=[Actions.HIGH_INTENSITY_PEAK_ANALYSIS.value, Actions.CELL_SORTER.value,
                                   DebugActions.FILESYSTEM_TEST.value, Actions.HELP.value, 'Exit'],
                          ),
        ]
    else:
        questions = [
            inquirer.List('action',
                          message="Choose Action?",
                          choices=[Actions.HIGH_INTENSITY_PEAK_ANALYSIS.value, Actions.CELL_SORTER.value,
                                   Actions.HELP.value, 'Exit'],
                          ),
        ]

    answers = inquirer.prompt(questions)

    answer = answers['action']
    if answer == Actions.HIGH_INTENSITY_PEAK_ANALYSIS.value:
        high_intensity_calculations.start_high_intensity_calculations()
        input('Press to continue...')
        start_up_actions()

    elif answer == Actions.CELL_SORTER.value:
        print('Not implemented yet')
        start_up_actions()
    elif answer == DebugActions.FILESYSTEM_TEST.value:
        write_high_stimulus_file([], 'test')
        start_up_actions()

    elif answer == Actions.HELP.value:
        webbrowser.open_new_tab('https://github.com/Exitare/High-Intensity-Peak-Analysis')

    elif answer == 'Exit':
        sys.exit(21)

    else:
        start_up_actions()


start()
