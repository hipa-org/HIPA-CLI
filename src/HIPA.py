import sys
from UI import Console
from Actions import Action_Handler
from Services.Config.Configuration import Config
import os
from Services.Config import Configuration, ArgumentParser
from Services.FileManagement import Folder_Management
import logging
from RuntimeConstants import Runtime_Datasets

logging.basicConfig(filename='log.log', level=logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
root = logging.getLogger()
root.setLevel(logging.DEBUG)
root.addHandler(handler)

if __name__ == "__main__":
    try:
        Configuration.read_conf()
        ArgumentParser.handle_args()

        if Folder_Management.create_required_folders():
            logging.info("All required folders generated.")
            logging.info("Please copy your files into the new folders and restart the application.")
            exit(0)
        else:
            logging.info("All folder checks passed.")
            logging.info("Creating evaluation folder.")
            Folder_Management.create_evaluation_folder()

        if Config.START_HIGH_INTENSITY_CALCULATION:
            Runtime_Datasets.Choice = 1
            Action_Handler.handle_choice()
        else:
            while True:
                Console.show_welcome_ui()
                Action_Handler.handle_choice()

    except KeyboardInterrupt:
        print('\n')
        try:
            sys.exit(0)

        except SystemExit:
            os._exit(0)
