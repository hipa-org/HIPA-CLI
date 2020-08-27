import datetime
from pathlib import Path
from Shared.Services.Configuration import Configuration_Service
from CLI.RuntimeConstants import Runtime_Folders
import sys
import shutil
import logging

folder_management = logging.getLogger()
folder_management.setLevel(logging.DEBUG)


def create_cli_evaluation_directory():
    """
    Creates the evaluation folder aka the root folder for each run of the application.
    :return:
    """

    config = Configuration_Service.get_config()

    now = datetime.datetime.now()
    path = Path(config.DataConfig.DATA_RESULTS_DIRECTORY, now.strftime('%Y-%m-%d-%H-%M-%S'))
    try:
        Path(path).mkdir(parents=True, exist_ok=True)

    except OSError as ex:
        folder_management.warning(f"Could not create evaluation directory {path}")
        folder_management.warning("Stopping application")
        if config.DEBUG:
            folder_management.warning(ex)
        sys.exit()
    else:
        Runtime_Folders.EVALUATION_DIRECTORY = path


def remove_folder(path):
    """
    Removes the folder with the given path
    """
    config = Configuration_Service.get_config()
    try:
        shutil.rmtree(path)
    except OSError as ex:
        folder_management.warning(f"Could not delete folder {path}")
        if config.GeneralConfig.DEBUG:
            folder_management.warning(ex)


def create_directory(path: str):
    """
    Creates a folder with the given path
    :param path:
    :return:
    """
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        print("Created directory")
        return path
    except OSError as ex:
        folder_management.critical(ex)
        folder_management.critical(f"Creation of the directory {path} failed.")
        folder_management.critical("Stopping application")
        sys.exit()


def create_required_folders():
    """
    Checks if the Data folder structure is up to date given the options from the config
    :return:
    """
    Config = Configuration_Service.get_config()

    created: bool = False

    folder_management.info("Checking data folder integrity...")
    if not Config.DataConfig.DATA_ROOT_DIRECTORY.is_dir():
        created = True
        folder_management.info("Root directory not found. Creating...")
        create_directory(Config.DataConfig.DATA_ROOT_DIRECTORY)

    if not Config.DataConfig.DATA_RAW_DIRECTORY.is_dir():
        created = True
        folder_management.info("Raw data directory not found. Creating...")
        create_directory(Config.DataConfig.DATA_RAW_DIRECTORY)

    if not Config.DataConfig.DATA_RESULTS_DIRECTORY.is_dir():
        created = True
        folder_management.info("Results data directory not found. Creating...")
        create_directory(Config.DataConfig.DATA_RESULTS_DIRECTORY)

    return created
