from enum import Enum
from pathlib import Path

# All files detected in the raw data folder
Files = []

# Choice made at the start
Choice = 0


class TimeFrameColumns(Enum):
    TIME_FRAME_VALUE = "Value"
    INCLUDING_MINUTE = "Including Minute"
    ABOVE_THRESHOLD = "Above Threshold"
