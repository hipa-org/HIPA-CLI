import os
from pyfiglet import Figlet
from platform import platform
from Shared.Services.Config.Configuration import Config
from CLI.RuntimeConstants import Runtime_Datasets


def print_empty_line():
    print()


def print_minus_line():
    print()
    print(30 * '-')
    print()


def clear_console():
    clear = None
    detected_os = platform(1, 1)
    print(detected_os)
    if "Darwin" in detected_os:
        clear = lambda: os.system('clear')
    elif "Windows" in detected_os:
        clear = lambda: os.system('cls')
    clear()


def print_hic_headline():
    clear_console()
    f = Figlet(font='slant')
    print(f.renderText('High Intensity Peak Analysis'))


def show_welcome_ui():
    """
    Displays the welcome ui
    """
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
            print()
            print('-1. Exit')

            if Config.DEBUG:
                print('** Debug **')
                print('F. File System Test')
            if Config.VERBOSE:
                print('Verbose active')

            Runtime_Datasets.Choice = int(input("Choose your action: (Type the action number)\n"))
        except ValueError:
            print("Please choose a valid option!")
            input()
            clear_console()
            show_welcome_ui()
        else:
            break

