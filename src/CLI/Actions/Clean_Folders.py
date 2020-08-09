from Shared.Services.Config.Configuration import Config
import os
import logging
from pathlib import Path
import shutil


def clean_folders():
    logging.info("Cleaning data folders...")

    for file in os.listdir(Config.DATA_RAW_DIRECTORY):
        try:
            os.remove(Path.joinpath(Config.DATA_RAW_DIRECTORY, file))
        except:
            logging.warning(f"Could not delete file {os.fsdecode(file)}!")

    for file in os.listdir(Config.DATA_RESULTS_DIRECTORY):
        shutil.rmtree(Path.joinpath(Config.DATA_RESULTS_DIRECTORY, file), ignore_errors=True)

    logging.info("Data folders cleaned up!")
