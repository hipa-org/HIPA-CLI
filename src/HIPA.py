import sys
from CLI.UI import Console
from CLI.Actions import Action_Handler
from Shared.Services.Config import Config, Configuration, ArgumentParser
import os
from Shared.Services.FileManagement import Folder_Management
import logging
from Shared.RuntimeConstants import Runtime_Datasets
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

logging.basicConfig(filename='log.log', level=logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
root = logging.getLogger()
root.setLevel(logging.DEBUG)
root.addHandler(handler)


def start_tool():
    """
    Starts the command line tool
    """
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


def start_web_server():
    """
    Starts the webserver
    """
    pass


if __name__ == "__main__":
    try:
        Configuration.read_conf()
        ArgumentParser.handle_args()

        if Config.START_WEB_SERVER:
            start_web_server()
        else:
            start_tool()


    except KeyboardInterrupt:
        print('\n')
        try:
            sys.exit(0)

        except SystemExit:
            os._exit(0)
