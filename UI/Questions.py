from UI.Console import print_hic_headline, clear_console
from Services.Config.Config import Config
from GlobalData import Statics
from Classes import InputFile
import os
from Services.Logger import Log

'''
Which Files should be processed
'''


def ask_files_to_process():
    print_hic_headline()
    all_files = os.listdir(os.path.normpath(Config.WORKING_DIRECTORY))
    temp_files = []
    for file in all_files:
        if Config.INPUT_FILE_NAME in file:
            if Config.OUTPUT_FILE_NAME_HIGH_STIMULUS not in file and Config.OUTPUT_FILE_NAME_NORMALIZED_DATA not in file:
                temp_files.append(file)

    print(
        'Choose all files you want to process.\n'
        '(Type each number separated by comma or just press enter to select all files)\n'
        'If you want to reload this windows to update the files type "r" and press enter!')
    print()
    i = 0
    for file in temp_files:
        print('{0}: {1}'.format(i, file))
        i += 1

    print()

    user_input = input('Select Files: ')

    if user_input.strip() == '':
        i = 0
        for file in temp_files:
            print("Selected File {0}".format(file))
            Statics.input_files.append(InputFile.InputFile(i, 0, 0, file, 0, list(), 0, list(), 0))
            i += 1
    else:
        for number in user_input.split(','):
            if number == 'r':
                ask_files_to_process()
            elif number.strip().isdigit() and int(number) < len(temp_files):
                Statics.input_files.append(
                    InputFile.InputFile(int(number), 0, 0, temp_files[int(number)], 0, list(), 0, list(), 0))
            else:
                print('Sorry but this file does not exist! Please try again!')
                input()
                ask_files_to_process()
    clear_console()
    return


'''
Ask for the Frame Number where the first stimulatory addition took place
'''


def ask_stimulation_time_frame():
    print_hic_headline()
    for file in Statics.input_files:
        print(file.name)
        print('Please insert the Stimulation Time Frame (0 - {0}) for the given file.'.format(
            len(file.cells[0].timeframes)))

        while True:
            try:
                file.stimulation_timeframe = int(input('Frame of stimulation for file {0}: '.format(file.name)))
            except ValueError:
                print("Sorry, but this is NOT a valid Integer. Please insert a valid one!")
                continue
            else:
                if file.stimulation_timeframe < 0 or file.stimulation_timeframe > len(file.cells[0].timeframes):
                    print("Sorry, but the stimulus is out of range! Please enter a valid one!")
                    continue
                else:
                    break
        print()

    clear_console()
    return


'''
Asks which files should be processed
'''


def ask_file_output():
    print_hic_headline()
    print('Which files should be created as Output?')
    print('Available Choices:\n')
    print('1. High Stimulus')
    print('2. Normalized Data')
    print()
    print('(Type each Number separated by comma or just press enter to select all options!)')
    user_choose = input()

    if user_choose.strip() == '':
        Statics.selected_output_options.append(Statics.OutputOptions.High_Stimulus.value)
        Statics.selected_output_options.append(Statics.OutputOptions.Normalized_Data.value)
        clear_console()
        return

    user_choose = user_choose.split(',')
    for choose in user_choose:
        if choose.isdigit():
            if int(choose.strip()) == 1:
                Statics.selected_output_options.append(Statics.OutputOptions.High_Stimulus.value)
            elif int(choose.strip()) == 2:
                Statics.selected_output_options.append(Statics.OutputOptions.Normalized_Data.value)
            else:
                Statics.selected_output_options.append(Statics.OutputOptions.High_Stimulus.value)
                Statics.selected_output_options.append(Statics.OutputOptions.Normalized_Data.value)

    clear_console()
    return


'''
Asks the User about the percentage which should be used
'''


def ask_percentage_limit():
    print_hic_headline()
    print("Please insert the Limit Percentage")
    print("This limit is calculated from the imputed maximum.")
    print("E.g. 0.6 is the 60%")
    print()
    for file in Statics.input_files:
        while True:
            try:
                file.percentage_limit = float(input('Percentage for file {0} (0 - 1): '.format(file.name)))
            except ValueError:
                print("Sorry but this is not a valid Float")
                continue
            else:
                if file.percentage_limit < 0.0 or file.percentage_limit > 1.0:
                    print("Sorry this is not a valid percentage")
                    continue
                else:
                    break

    clear_console()



'''
Prints a conclusion before starting the Calculations
'''


def conclusion():
    print_hic_headline()
    Log.write_message("You selected the following output options:", Log.LogLevel.Info)
    for output in Statics.selected_output_options:
        Log.write_message(output, Log.LogLevel.Info)

    print()
    for file in Statics.input_files:
        Log.write_message(
            'You are processing the File {0} with following arguments: \nStimulation Timeframe: {1}\nPercentage: {2}'.format(
                file.name, file.stimulation_timeframe, file.percentage_limit), Log.LogLevel.Info)
        print()

    input("Press any Key to start Calculations.")
