from enum import Enum


class Actions(Enum):
    HIGH_INTENSITY_PEAK_ANALYSIS = 'High Intensity Peak Analysis'
    CELL_SORTER = 'Cell Sorter'
    HELP = 'Help'


class DebugActions(Enum):
    FILESYSTEM_TEST = 'File System Test'


class NormalizationMethods(Enum):
    Baseline = "Baseline"
    To_One = "ToOne"


class Choices(Enum):
    HIGH_INTENSITY = 1
    CELL_SORTER = 2
    HELP = 3
    CLEAN_FOLDER = 4
