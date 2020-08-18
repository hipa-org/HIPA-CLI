import os
from Shared.Services.Config.Configuration import Config
from CLI.RuntimeConstants import Runtime_Datasets
import logging
from Shared.Classes.File import File
from Shared.Classes.Folder import Folder
from Web.RuntimeConstants import Folders


def load_cli_raw_files():
    """
    Loads all raw data sets from the given raw directory
    """
    for file in os.listdir(Config.DATA_RAW_DIRECTORY):
        file_name = os.fsdecode(file)
        try:
            if file_name.endswith("txt"):
                Runtime_Datasets.Files.append(File(file_name))

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
