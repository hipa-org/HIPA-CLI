import os
from Shared.Services.Config.Configuration import Config
from CLI.RuntimeConstants import Runtime_Datasets
import logging
from pathlib import Path
import pandas as pd
import sys


class DataLoader:
    @staticmethod
    def load_cli_raw_files() -> []:
        """
        Loads all raw data sets from the given raw directory
        """
        files = []
        for file in os.listdir(Config.DATA_RAW_DIRECTORY):
            file_name = os.fsdecode(file)
            try:
                if file_name.endswith("txt") or file_name.endswith("csv"):
                    files.append(file)

            except OSError as ex:
                logging.warning(ex)
            except BaseException as ex:
                logging.warning(ex)

    @staticmethod
    def load_file(path: str):
        """
        Reads the content of the given path into a pandas data frame
        """
        try:
            if path.endswith("csv"):
                return pd.read_csv(path, header=0)

            return pd.read_csv(path, sep="\t", header=0)
        except FileNotFoundError as ex:
            logging.error(f'Could not locate file {path}')
            logging.error(ex)
            sys.exit(21)
