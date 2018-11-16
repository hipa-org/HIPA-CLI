import sys
import argparse
from pyfiglet import Figlet
import inquirer
from enum import Enum
import actions
import config


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

    args = vars(ap.parse_args())
    handle_args(args)
    start_up_actions()


def handle_args(arguments):

    if arguments['verbose']:
        config.config.verbose_mode = True
    else:
        config.config.verbose_mode = False

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
