import os
from Services.Config.Configuration import Config
from RuntimeConstants import Runtime_Datasets
import logging
from Classes.File import File


def load_raw_files():
    for file in os.listdir(Config.DATA_RAW_DIRECTORY):
        file_name = os.fsdecode(file)
        try:
            if file_name.endswith("txt"):
                Runtime_Datasets.Files.append(File(file_name))

        except OSError as ex:
            logging.warning(ex)
        except BaseException as ex:
            logging.warning(ex)

