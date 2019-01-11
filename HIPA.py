import sys
import argparse
from pyfiglet import Figlet
from enum import Enum
from actions import high_intensity_calculations
from services.config.config import Config, read_conf, reset_config
import os
from services.logger.log import write_message, LogLevel
from services.filemanagement.create_files import create_needed_files
import webbrowser
from UI.UI import clear_console


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
    ap.add_argument("-D", "--debug", required=False,
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
    clear_console()

    while True:
        try:
            f = Figlet(font='slant')
            print(f.renderText('Intensity Analyzer'))
            print(30 * '-')
            print('1. High Intensity Peak Analysis ')
            print('2. Cell Sorter')
            print('3. Help')
            print('4. Cleanup Output Folder')
            print('-1. Exit')

            if Config.DEBUG == 1:
                print('** Debug **')
                print('F. File System Test')

            choice = int(input("Choose your action: (Type the action number)\n"))
        except ValueError:
            print("Please choose a valid option!")
            input()
            clear_console()
            continue
        else:
            break

    if choice == 1:
        high_intensity_calculations.start_high_intensity_calculations()
        input('Press key to continue...')
        start_up_actions()
    elif choice == 2:
        print('Not implemented yet')
        input('Press key to continue...')
        start_up_actions()
    elif choice == 3:
        webbrowser.open_new_tab('https://exitare.github.io/High-Intensity-Peak-Analysis/')
        start_up_actions()
    elif choice == -1:
        clear_console()
        sys.exit(0)
    else:
        start_up_actions()


if __name__ == "__main__":
    try:
        start()
    except KeyboardInterrupt:
        print('\n')
        try:
            sys.exit(0)

        except SystemExit:
            os._exit(0)
