from Shared.Services.FileManagement import Folder_Management
import logging
from Shared.Services.Config import Configuration
from CLI.RuntimeConstants import Runtime_Datasets
from CLI.Actions import Action_Handler
from CLI.UI import Console


def start_cli_tool():
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
        Folder_Management.create_cli_evaluation_directory()

    if Configuration.Config.START_HIGH_INTENSITY_CALCULATION:
        Runtime_Datasets.Choice = 1
        Action_Handler.handle_choice()
    else:
        while True:
            Console.show_welcome_ui()
            Action_Handler.handle_choice()
