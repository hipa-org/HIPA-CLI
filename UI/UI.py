import os
from pyfiglet import Figlet
from platform import platform


def print_empty_line():
    print()


def print_minus_line():
    print()
    print(30 * '-')
    print()


def clear_console():
    clear = None
    detected_os = platform(1, 1)
    if "Darwin" in detected_os:
        clear = lambda: os.system('clear')
    elif "win32" in detected_os:
        clear = lambda: os.system('cls')
    clear()


def print_hic_headline():
    clear_console()
    f = Figlet(font='slant')
    print(f.renderText('High Intensity Peak Analysis'))
