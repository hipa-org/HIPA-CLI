from CLI.RuntimeConstants import Runtime_Datasets
from CLI.Enums import Actions
from CLI.Actions import High_Intensity_Calculations, Clean_Folders
import webbrowser
import sys
import logging
from Shared.Services.DataLoader import Data_Loader


def handle_choice():
    """
    Handles the choice a user types into console
    """
    if Runtime_Datasets.Choice == Actions.Choices.HIGH_INTENSITY.value:
        Data_Loader.load_cli_raw_files()

        if len(Runtime_Datasets.Files) == 0:
            logging.info("No files detected!")
            input()
            return
        else:
            logging.info(f"Detected {len(Runtime_Datasets.Files)} files!")

        High_Intensity_Calculations.start_high_intensity_calculations()
    elif Runtime_Datasets.Choice == Actions.Choices.CELL_SORTER.value:
        print('Not implemented yet')
        input('Press key to continue...')
    elif Runtime_Datasets.Choice == Actions.Choices.HELP.value:
        webbrowser.open_new_tab('https://github.com/Exitare/HIPA-CLI')
    elif Runtime_Datasets.Choice == Actions.Choices.CLEAN_FOLDER.value:
        Clean_Folders.clean_folders()
        input()

    elif Runtime_Datasets.Choice == -1:
        sys.exit(0)
    else:
        logging.warning("Invalid choice detected. Stopping.")
        sys.exit(0)

    Runtime_Datasets.choice = 0
