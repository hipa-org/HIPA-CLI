from CLI.UI.Console import print_hic_headline, clear_console
from Shared.Services.Config.Configuration import Config
from CLI.RuntimeConstants import Runtime_Datasets
import logging
from Shared.Classes import File


def ask_stimulation_time_frames():
    """
    Ask for the Frame Number where the first stimulatory addition took place
    """
    print_hic_headline()
    print(f'Please specify the Stimulation Time Frame(s) for each file.')
    print(f'You can add as many time frames as you like. Just separate them by comma.')
    print(f'Example: 372,696,1091')
    print()
    for file in Runtime_Datasets.Files:
        while True:
            print()
            print(
                f'Please specify the Stimulation Time Frame (0 - {len(file.cells[0].time_frames)}) '
                f'for the file {file.name}:')

            frames: str = input(f'Frame of stimulation for file {file.name}: ')
            frames: list = frames.split(',')
            for frame in frames:
                try:
                    frame = int(frame)
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
    print("Please insert the threshold.")
    print("The threshold is defined as the value as of which a peak is going to be considered a high intensity peak.")
    print("E.g. 0.6 is 60% of the maximum intensity detected in your data.")
    print()

    # Iterating through given files
    file: File
    for file in Runtime_Datasets.Files:
        while True:
            try:
                file.high_intensity_threshold = float(input(f'Spike threshold for file {file.name} (0 - 1): '))
            except ValueError:
                print("Sorry but this is not a valid percentage.")
                continue
            else:
                if file.high_intensity_threshold < 0.0 or file.high_intensity_threshold > 1.0:
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
            f'You are processing the file {file.name} with following arguments: \nStimulation Time frames:'
            f' {file.stimulation_time_frames}\nPercentage: {file.threshold}')
        print()

    input("Press any Key to start Calculations.")
