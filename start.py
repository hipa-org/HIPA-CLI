import sys
import argparse
from pyfiglet import Figlet
import inquirer
from enum import Enum
import actions
import services
from services.logger.log import LogLevel, write_message
from services.config.config import Config, read_conf

class Actions(Enum):
    HIGH_INTENSITY_PEAK_ANALYSIS = 'High Intensity Peak Analysis'
    CELL_SORTER = 'Cell Sorter'


class DebugActions(Enum):
    FILESYSTEM_TEST = 'File System Test'


def start():
    ap = argparse.ArgumentParser()
    ap.add_argument("-V", "--verbose", required=False,
                    action='store_true',
                    help="Activate verbose Output")
    ap.add_argument("-C", "--calculate", required=False,
                    action='store_true',
                    help='Direct call of calculation')
    ap.add_argument("-d", "--debug", required=False,
                    action='store_true',
                    help="Starts the program in Debug Mode")

    args = vars(ap.parse_args())
    handle_args(args)
    success = read_conf()
    if success is not True:
        write_message(success, LogLevel.Warn)
    start_up_actions()


def handle_args(arguments):
    if arguments['verbose']:
        services.config.config.Config.VERBOSE = 1

    if arguments['calculate']:
        actions.high_intensity_calculations.start_high_intensity_calculations()
        sys.exit(21)

    if arguments['debug']:
        services.config.config.Config.DEBUG = 1
        write_message('IMPORTANT NOTICE: DEBUG MODE IS ACTIVE!', LogLevel.Info)

    write_message('Arguments {0}'.format(arguments), LogLevel.Verbose)


def start_up_actions():
    if Config.DEBUG == 1:
        questions = [
            inquirer.List('action',
                          message="Choose Action?",
                          choices=[Actions.HIGH_INTENSITY_PEAK_ANALYSIS.value, Actions.CELL_SORTER.value,
                                   DebugActions.FILESYSTEM_TEST.value, 'Exit'],
                          ),
        ]
    else:
        questions = [
            inquirer.List('action',
                          message="Choose Action?",
                          choices=[Actions.HIGH_INTENSITY_PEAK_ANALYSIS.value, Actions.CELL_SORTER.value, 'Exit'],
                          ),
        ]

    answers = inquirer.prompt(questions)

    answer = answers['action']
    if answer == Actions.HIGH_INTENSITY_PEAK_ANALYSIS.value:
        actions.high_intensity_calculations.start_high_intensity_calculations()

    elif answer == Actions.CELL_SORTER.value:
        print('Not implemented yet')
    elif answer == DebugActions.FILESYSTEM_TEST.value:
        services.files.write_files.write_results_file([])
    elif answer == 'Exit':
        sys.exit(21)

    else:
        start_up_actions()


f = Figlet(font='slant')
print(f.renderText('Intensity Analyzer'))

start()
