from CLI.RuntimeConstants.Runtime_Datasets import TimeFrameColumns
import pandas as pd


class Cell:
    def __init__(self, name: str):
        self.name = name
        self.time_frames = pd.DataFrame()
        self.baseline_mean: float = 0
        self.time_frame_maximum: float = 0
        self.normalized_time_frames = pd.DataFrame()
        self.normalized_baseline_mean: float = 0
        self.true_signal_threshold: float = 0
        self.high_intensity_counts = pd.DataFrame()
        self.intervals = pd.DataFrame()
        self.interval_high_intensity_counts_previous_interval = pd.DataFrame()
        self.interval_high_intensity_counts_compared_to_baseline = pd.DataFrame()

    def create_intervals(self, stimulation_time_frames):
        """
        Splits each cell into intervals for further evaluation
        """
        frames = []
        last_time_frame: int = 0
        for selected_time_frame in stimulation_time_frames:
            if last_time_frame == 0:
                last_time_frame = selected_time_frame
                frames.append(self.normalized_time_frames[:selected_time_frame])
            else:
                frames.append(self.normalized_time_frames[last_time_frame:selected_time_frame])
                last_time_frame = selected_time_frame
        else:
            frames.append(self.normalized_time_frames[last_time_frame:])

        self.intervals = frames

    def calculate_high_stimulus_count(self, baseline: bool):
        """
        Counts the amount of high intense stimuli compared to the previous interval or compared to the baseline interval
        """
        interval_counts = pd.DataFrame(columns=['Count', 'Activation'])

        # Counter for loop
        i = 0

        if baseline:
            compare_high_intensity_counts = len(
                self.intervals[0].loc[self.intervals[0][TimeFrameColumns.HIGH_INTENSITY.value] == True].index)
        else:
            compare_high_intensity_counts = 0
        for interval in self.intervals:
            high_intensity_count = len(interval.loc[interval[TimeFrameColumns.HIGH_INTENSITY.value] == True].index)

            # Initial interval
            if i == 0:
                interval_counts = interval_counts.append({'Count': high_intensity_count, 'Activation': False},
                                                         ignore_index=True)
            # All following intervals
            else:
                if high_intensity_count > compare_high_intensity_counts:
                    interval_counts = interval_counts.append({'Count': high_intensity_count, 'Activation': True},
                                                             ignore_index=True)
                else:
                    interval_counts = interval_counts.append({'Count': high_intensity_count, 'Activation': False},
                                                             ignore_index=True)

            if not baseline:
                compare_high_intensity_counts = high_intensity_count
            i += 1

        if baseline:
            self.interval_high_intensity_counts_compared_to_baseline = interval_counts
        else:
            self.interval_high_intensity_counts_previous_interval = interval_counts
