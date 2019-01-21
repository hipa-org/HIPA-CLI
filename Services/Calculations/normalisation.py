from Classes import InputFile

'''
Normalize each Datapoint in Cell
'''


def normalise_timeframes(file: InputFile):
    temp_timeframes = list()
    for cells in file.cells:
        i = 0
        for timeframe in cells.timeframes[:file.stimulation_timeframe]:
            i += 1
            temp_timeframes.append(timeframe)

        else:
            cells.normalized_timeframes = temp_timeframes
            print(i)
