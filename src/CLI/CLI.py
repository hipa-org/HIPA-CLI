import logging
from Shared.Services.Config import Configuration
from CLI.RuntimeConstants import Runtime_Datasets
from Shared.Services.DataHandler.Data_Loader import DataLoader
import webbrowser
from Shared.Services.FileManagement.Folder_Management import FolderManagement
from Enums.Actions import Actions
from CLI.UI import Console, Questions
from Shared.Entities.file import File
import sys
import datetime


class CLI:
    # All detected files in the data folder
    detected_files = []
    # All file entities
    files = []

    def __init__(self):
        """
               Starts the command line tool
               """
        if FolderManagement.create_required_folders():
            logging.info("All required folders generated.")
            logging.info("Please copy your files into the new folders and restart the application.")
            exit(0)
        else:
            logging.info("All folder checks passed.")
            logging.info("Creating evaluation folder.")
            FolderManagement.create_cli_evaluation_directory()

        while True:
            Console.show_welcome_ui()
            self.handle_choice()

    def handle_choice(self):
        """
        Handles the choice a user types into console
        """
        if Runtime_Datasets.Choice == Actions.Choices.HIGH_INTENSITY.value:
            self.detected_files = DataLoader.load_cli_raw_files()

            if len(self.detected_files) == 0:
                logging.info("No files detected!")
                input()
                return
            else:
                logging.info(f"Detected {len(self.detected_files)} files!")

            # Load all files into memory
            for detected_file in self.detected_files:
                self.files.append(File(detected_file))

            self.start_high_intensity_calculations()

        elif Runtime_Datasets.Choice == Actions.Choices.CELL_SORTER.value:
            print('Not implemented yet')
            input('Press key to continue...')
        elif Runtime_Datasets.Choice == Actions.Choices.HELP.value:
            webbrowser.open_new_tab('https://github.com/Exitare/HIPA-CLI')
        elif Runtime_Datasets.Choice == Actions.Choices.CLEAN_FOLDER.value:
            logging.info("Cleaning data folders...")
            FolderManagement.clean_folders()
            logging.info("Data folders cleaned up!")
            input()

        elif Runtime_Datasets.Choice == -1:
            sys.exit(0)
        else:
            logging.warning("Invalid choice detected. Stopping.")
            sys.exit(0)

        Runtime_Datasets.choice = 0

    def start_high_intensity_calculations(self):
        """
        High Intensity Calculations done here.
        :return:
        """

        Questions.ask_stimulation_time_frames()
        Questions.ask_threshold()
        Questions.conclusion()

        for input_file in self.files:
            print()
            logging.info(f'Processing file {input_file.name}')
            self.execute_high_intensity_calculation(input_file)

        return True

    def execute_high_intensity_calculation(self, file: File):
        """
        Executed the high intensity calculations for each file
        """
        start_time = datetime.datetime.now()
        file.calculate_baseline_mean()
        file.normalize_time_frames_with_to_ones()
        file.calculate_normalized_baseline_mean()
        file.calculate_time_frame_maximum()
        file.calculate_true_signal_threshold()
        file.detect_true_signal()
        file.detect_high_intensity_signal()
        file.count_high_intensity_peaks_per_minute()
        file.summarize_high_intensity_peaks()
        file.split_cells()
        file.calculate_high_stimulus_count_per_interval()
        file.generate_reports()
        file.plot_graphs()

        end_time = datetime.datetime.now()
        logging.info(f'Evaluation of file {file.name} done.')
        logging.info(f'Calculation done in {end_time - start_time} seconds.')
        logging.info(f'{len(file.cells) * len(file.cells[0].time_frames)} time frames processed')
