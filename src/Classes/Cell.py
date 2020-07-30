from RuntimeConstants.Runtime_Datasets import TimeFrameColumns
import pandas as pd


class Cell:
    def __init__(self, name: str):
        self.name = name
        self.time_frames = pd.DataFrame()
        self.baseline_mean = 0
        self.time_frame_maximum = 0
        self.normalized_time_frames = pd.DataFrame()
        self.threshold = 0
        self.high_intensity_counts = pd.DataFrame()
        self.intervals = pd.DataFrame()
        self.interval_high_intensity_counts = pd.DataFrame()

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

