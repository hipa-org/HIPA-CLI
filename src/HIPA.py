import sys
from CLI.UI import Console
from CLI.Actions import Action_Handler
from Shared.Services.Config import Configuration, ArgumentParser
import os
from Shared.Services.FileManagement import Folder_Management
import logging
from Shared.RuntimeConstants import Runtime_Datasets
from flask import Flask
from flask_restful import Resource, Api
from waitress import serve
from Web.Controller.HomeController import HomeController
from Web.Controller.UploadController import UploadController
from Web.Controller.ToolController import ToolController

app = Flask(__name__, template_folder="./Web/Static/Templates")
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

    if Configuration.Config.START_HIGH_INTENSITY_CALCULATION:
        Runtime_Datasets.Choice = 1
        Action_Handler.handle_choice()
    else:
        while True:
            Console.show_welcome_ui()
            Action_Handler.handle_choice()


def start_web_server():
    """
    Starts the web server
    """
    logging.info("Starting the HIPA tool in web server mode...")
    load_api()
    serve(app, host='0.0.0.0', port=15000, threads=16)


def load_api():
    logging.info("Loading api controllers...")
    api.add_resource(HomeController, '/')
    api.add_resource(UploadController, '/upload')
    api.add_resource(ToolController, '/tool')


if __name__ == "__main__":
    try:
        Configuration.read_conf()
        ArgumentParser.handle_args()

        if Configuration.Config.START_WEB_SERVER:
            start_web_server()
        else:
            start_tool()


    except KeyboardInterrupt:
        print('\n')
        try:
            sys.exit(0)

        except SystemExit:
            os._exit(0)
