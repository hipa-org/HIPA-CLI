import sys
import os
from sys import platform

CURSOR_UP_ONE = "\033[F"
ERASE_LINE = "\033[K"

sys.stdout.write(CURSOR_UP_ONE)
sys.stdout.write(ERASE_LINE)


def delete_last_lines(n=1):
    print("fuck it")
    for _ in range(n):
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)


def clear_console():
    clear = None
    if platform == "linux" or platform == "linux2":
        clear = lambda: os.system('clear')
    elif platform == "darwin":
        clear = lambda: os.system('clear')
    elif platform == "win32":
        clear = lambda: os.system('cls')
    clear()
