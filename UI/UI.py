import os
from pyfiglet import Figlet


def print_empty_line():
    print()


def print_minus_line():
    print()
    print(30 * '-')
    print()


def clear_console():
    clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
    clear()


def print_hic_headline():
    clear_console()
    f = Figlet(font='slant')
    print(f.renderText('High Intensity Peak Analysis'))
