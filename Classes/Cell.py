from Classes import InputFile, TimeFrame


class Cell:
    def __init__(self, name: str, timeframes: list, threshold: float, baseline_mean: float, normalized_timeframes: list,
                 timeframe_maximum: float, high_intensity_counts: dict):
        self.name = name
        self.timeframes = timeframes
        self.baseline_mean = baseline_mean
        self.timeframe_maximum = timeframe_maximum
        self.normalized_timeframes = normalized_timeframes
        self.threshold = threshold
        self.high_intensity_counts = high_intensity_counts
