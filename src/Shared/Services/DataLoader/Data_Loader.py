import os
from Shared.Services.Configuration import Configuration_Service, CLI_Configuration
from CLI.RuntimeConstants import Runtime_Datasets
import logging
from Shared.Classes.File import File
from Shared.Classes.Folder import Folder
from Web.RuntimeConstants import Folders
from pathlib import Path
import traceback


def load_cli_raw_files():
    """
    Loads all raw data sets from the given raw directory
    """
    config = Configuration_Service.get_config()

    # Clear array for each run
    Runtime_Datasets.Files = []
    try:
        # Get all files inside the raw directory
        for file in os.listdir(Path(config.DataConfig.DATA_RAW_DIRECTORY)):
            if file.endswith("txt"):
                Runtime_Datasets.Files.append(File(Path(config.DataConfig.DATA_RAW_DIRECTORY, file)))

        # Get all files inside subfolders located in the raw directory
        for root, dirs, files in os.walk(config.DataConfig.DATA_RAW_DIRECTORY):
            for dir in dirs:
                for file in os.listdir(Path.joinpath(config.DataConfig.DATA_RAW_DIRECTORY, dir)):
                    if file.endswith("txt"):
                        Runtime_Datasets.Files.append(File(Path(config.DataConfig.DATA_RAW_DIRECTORY, dir, file)))

    except OSError as ex:
        logging.warning(ex)

    except BaseException as ex:
        logging.warning(ex)


def find_evaluation_folder(evaluation_folder_name: str) -> Folder:
    """
    Finds the folder associated to the name
    """
    for folder in Folders.folders:
        if folder.name == evaluation_folder_name:
            return folder

    return None


def load_folders():
    """
    Loads all raw folders for the web application
    """
    config = Configuration_Service.get_config()
    try:
        print("Loading folders...")
        for root, dirs, files in os.walk(config.DataConfig.DATA_RAW_DIRECTORY):
            for dir in dirs:
                files = []
                for file in os.listdir(Path.joinpath(config.DataConfig.DATA_RAW_DIRECTORY, dir)):
                    if file.endswith("txt"):
                        new_file: File = File(Path(config.DataConfig.DATA_RAW_DIRECTORY, dir, file))
                        print(new_file.path)
                        files.append(new_file)

                Folders.folders.append(Folder(dir, files))

        for folder in Folders:
            for file in folder.files:
                print(file.name)
                print(file.path)


    except BaseException as ex:
        logging.exception(ex)
