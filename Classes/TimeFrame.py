class Timeframe:
    def __init__(self, identifier: int, value: float, including_minute: int, above_threshold: bool):
        self.identifier = identifier
        self.value = value
        self.including_minute = including_minute
        self.above_threshold = above_threshold
