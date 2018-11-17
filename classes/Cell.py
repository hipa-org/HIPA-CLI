class Cell:
    def __init__(self, name, baseline_mean, all_mean, normalized_data, maximum, limit, over_under_limit,
                 high_stimulus_per_minute):
        self.name = name
        self.baseline_mean = baseline_mean
        self.mean = all_mean
        self.maximum = maximum
        self.normalized_data = normalized_data
        self.limit = limit
        self.over_under_limit = over_under_limit
        self.high_stimulus_per_minute = high_stimulus_per_minute
