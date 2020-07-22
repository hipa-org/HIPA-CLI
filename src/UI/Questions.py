from UI.Console import print_hic_headline, clear_console
from Services.Config.Configuration import Config
from RuntimeConstants import Runtime_Datasets
import logging


def ask_stimulation_time_frames():
    """
    Ask for the Frame Number where the first stimulatory addition took place
    """
    print_hic_headline()
    for file in Runtime_Datasets.Files:
        print(f'Please specify the Stimulation Time Frame (0 - {len(file.cells[0].time_frames)}) for the given file.')

        while True:
            frames: str = input(f'Frame of stimulation for file {file.name}: ')
            frames: list = frames.split(',')
            for frame in frames:
                try:
                    frame = int(frame)
                    print(frame)
                    if frame < 0 or frame > len(file.cells[0].time_frames):
                        print(
                            "Sorry, but the stimulation appears to be out of range! Ignoring time frame!")
                        continue

                    file.stimulation_time_frames.append(int(frame))
                except ValueError:
                    print("Sorry, but this is NOT a valid Integer. Ignoring time frame!")
                    continue

            else:
                if len(file.stimulation_time_frames) == 0:
                    ask_stimulation_time_frames()
                break

    clear_console()
    return


def ask_threshold():
    """
    Asks the User about the percentage which should be used
    """
    print_hic_headline()
    print("Please insert the threshold")
    print("This limit is calculated from the imputed maximum.")
    print("E.g. 0.6 is the 60%")
    print()

    # Iterating through given files
    for file in Runtime_Datasets.Files:
        while True:
            try:
                file.threshold = float(input(f'Percentage for file {file.name} (0 - 1): '))
            except ValueError:
                print("Sorry but this is not a valid percentage.")
                continue
            else:
                if file.threshold < 0.0 or file.threshold > 1.0:
                    print("Sorry this is not a valid percentage")
                    continue
                else:
                    break

    clear_console()


def conclusion():
    """
    Prints a conclusion before starting the Calculations
    """

    print_hic_headline()
    logging.info('Normalization method: {0}'.format(Config.NORMALIZATION_METHOD))
    print()
    for file in Runtime_Datasets.Files:
        logging.info(
            f'You are processing the File {file.name} with following arguments: \nStimulation Timeframes:'
            f' {file.stimulation_time_frames}\nPercentage: {file.threshold}')
        print()

    input("Press any Key to start Calculations.")