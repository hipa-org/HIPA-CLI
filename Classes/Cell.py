class Cell:
    def __init__(self, name, timeframes,threshold, baseline_mean, normalized_timeframes, timeframe_maximum,  high_intensity_counts):
        self.name = name
        self.timeframes = timeframes
        self.baseline_mean = baseline_mean
        self.timeframe_maximum = timeframe_maximum
        self.normalized_timeframes = normalized_timeframes
        self.threshold = threshold
        self.high_intensity_counts = high_intensity_counts
