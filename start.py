import re
import numpy as np
import os.path
from enum import Enum
from random import randint


class Paths(Enum):
    SAMPLE_DIR = 'sampleData/'
    INPUT_DIR = 'Input/'
    OUTPUT_DIR = 'Output/'
    OUTPUT_FILE_NAME = 'Results.txt'
    OUTPUT_PATH = 'Output/Results.txt'


class PlotValue:
    def __init__(self, id, number):
        self.id = id
        self.number = number


class Cell:

    def __init__(self, id, mean):
        self.id = id
        self.mean = mean


plot_values = open("sampleData/plot_values.txt", "r").read().splitlines()
plotValueArray = []
splitPlotValueArray = []

## Plot Values
for i in plot_values:
    splitPlotValueArray.append((i.split('\t', 1)))

for i in splitPlotValueArray:
    plotValueArray.append(PlotValue(i[0], i[1]))

## Plot Values End


##Time Traces


timeTracesFileData = open("sampleData/time_traces.txt", "r")
rows = (row.strip().split() for row in timeTracesFileData)
timeTraces = zip(*(row for row in rows if row))
timeTracesFileData.close()

CellData = []

rowCount = 0
detectedColumns = 0
counter = 0
for timeTrace in timeTraces:
    counter = 0
    for timeData in timeTrace[1:]:
        rowCount = float(timeData) + rowCount
        counter += 1

    else:
        detectedColumns += 1
        mean = np.mean(rowCount, dtype=np.float64)
        CellData.append(Cell(timeTrace[0], mean))

print('Detected Headers including Avg and Err Column: ', detectedColumns)

print(Paths.OUTPUT_PATH.value)

fileExists = os.path.exists(Paths.OUTPUT_PATH.value)

print(fileExists)
if fileExists:
    os.remove(Paths.OUTPUT_PATH.value)

fh = open(Paths.OUTPUT_PATH.value, "w")
writtenColumns = 0

for cell in CellData:
    temp = 'ID: %s :  Mean: %d ' % (cell.id, cell.mean)
    fh.write(temp)
    writtenColumns += 1
fh.close()

print('Creating File %s' % Paths.OUTPUT_PATH.value)
print('Written Columns: ', writtenColumns)
