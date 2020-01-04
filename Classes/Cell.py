from GlobalData.Statics import TimeFrameColumns


class Cell:
    def __init__(self, name: str, time_frames: list, threshold: float, baseline_mean: float,
                 normalized_time_frames: list,
                 time_frame_maximum: float, high_intensity_counts: list, intervals: list,
                 interval_high_intensity_counts):
        self.name = name
        self.time_frames = time_frames
        self.baseline_mean = baseline_mean
        self.time_frame_maximum = time_frame_maximum
        self.normalized_time_frames = normalized_time_frames
        self.threshold = threshold
        self.high_intensity_counts = high_intensity_counts
        self.intervals = intervals
        self.interval_high_intensity_counts = interval_high_intensity_counts

    def split_cells(self, stimulation_time_frames):
        frames = []
        last_split: int = 0
        for split in stimulation_time_frames:
            if last_split == 0:
                last_split = split
                frames.append(self.normalized_time_frames[:split])
            else:
                frames.append(self.normalized_time_frames[last_split:split])
                last_split = split
        else:
            frames.append(self.normalized_time_frames[last_split:])
        self.intervals = frames

    def calculate_high_stimulus_count_per_interval(self):
        interval_counts = []
        for interval in self.intervals:
            df = interval.groupby(TimeFrameColumns.INCLUDING_MINUTE.value)[
                TimeFrameColumns.ABOVE_THRESHOLD.value].apply(
                lambda x: (x == True).sum()).reset_index()
            del df[TimeFrameColumns.INCLUDING_MINUTE.value]
            df.columns = ['Count']
            interval_counts.append(df['Count'].sum())
        self.interval_high_intensity_counts = interval_counts

        # print(df)
