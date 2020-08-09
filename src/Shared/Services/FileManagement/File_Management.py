from pathlib import Path
import ntpath
from Shared.Services import Config
import pandas as pd


def get_file_name(path):
    """
    Returns the filename
    :param path:
    :return:
    """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def read_file(path: str):
    """
    Reads the file located at the given path
    :param path:
    :return:
    """
    try:
        return pd.read_csv(f"{Config.DATA_RAW_DIRECTORY}/{path}")
    except OSError as ex:
        if Config.VERBOSE:
            print(ex)
        return None


def create_csv_file(df, folder, name):
    """
    Writes a df to a given folder with the given name
    :param df:
    :param folder:
    :param name:
    :return:
    """
    if folder != "" and not df.empty:
        path = Path.joinpath(folder, f"{name}.csv")
        df.to_csv(path, index=True)