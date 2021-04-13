from enum import Enum
from pathlib import Path


# Choice made at the start
Choice = 0


class TimeFrameColumns(Enum):
    TIME_FRAME_VALUE = "Value"
    INCLUDING_MINUTE = "Including Minute"
    TRUE_SIGNAL = "True Signal"
    HIGH_INTENSITY = "Spike"
