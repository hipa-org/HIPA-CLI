import sys
import argparse
from pyfiglet import Figlet
import inquirer
from enum import Enum
import actions
import services


class Actions(Enum):
    CALCULATE_DATA = 'Calculate Data'
    INPUT_DIR = 'Input/'
    OUTPUT_DIR = 'Output/'
    OUTPUT_FILE_NAME = 'Results.txt'
    OUTPUT_PATH = 'Output/Results.txt'


def start():
    ap = argparse.ArgumentParser()
    ap.add_argument("-V", "--verbose", required=False,
                    action='store_true',
                    help="Activate verbose Output")
    ap.add_argument("-C", "--calculate", required=False,
                    action='store_true',
                    help='Direct call of calculation')
    ap.add_argument("-d", "--debug", required=False,
                    help="Starts the program in Debug Mode")

    args = vars(ap.parse_args())
    handle_args(args)
    services.config.config.check_config()
    start_up_actions()


def handle_args(arguments):
    #print(services.config.config.configs['SETTINGS'])
    if arguments['verbose']:
        services.config.config.configs['settings']['verbose'] = 1
    else:
        services.config.verbose_mode = False


    if arguments['calculate']:
        actions.calculate_data.calculate_data()
        sys.exit(21)


def start_up_actions():
    questions = [
        inquirer.List('action',
                      message="Choose Action?",
                      choices=[Actions.CALCULATE_DATA.value, 'Exit'],
                      ),
    ]
    answers = inquirer.prompt(questions)

    answer = answers['action']
    if answer == Actions.CALCULATE_DATA.value:
        actions.calculate_data.calculate_data()

    elif answer == 'Exit':
        sys.exit(21)


f = Figlet(font='slant')
print(f.renderText('Data Calculator'))

start()
