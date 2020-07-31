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

    def create_intervals(self, stimulation_time_frames):
        """
        Splits each cell into intervals for further evaluation
        """
        frames = []
        last_time_frame: int = 0
        for time_frame in stimulation_time_frames:
            if last_time_frame == 0:
                last_time_frame = time_frame
                frames.append(self.normalized_time_frames[:time_frame])
            else:
                frames.append(self.normalized_time_frames[last_time_frame:time_frame])
                last_time_frame = time_frame
        else:
            frames.append(self.normalized_time_frames[last_time_frame:])

        self.intervals = frames

    def calculate_high_stimulus_count_per_interval(self):
        """
        Counts the amount of high intense stimuli for each interval and compares it to the previous one
        """
        interval_counts = pd.DataFrame(columns=['Counts', 'Activation'])

        # Counter for loop
        i = 0
        previous_high_intensity_counts = 0
        for interval in self.intervals:
            high_intensity_count = len(interval.loc[interval[TimeFrameColumns.ABOVE_THRESHOLD.value] == True].index)

            # Initial interval
            if i == 0:
                interval_counts = interval_counts.append({'Counts': high_intensity_count, 'Activation': False},
                                                         ignore_index=True)
            # All following intervals
            else:
                if high_intensity_count > previous_high_intensity_counts:
                    interval_counts = interval_counts.append({'Counts': high_intensity_count, 'Activation': True},
                                                             ignore_index=True)
                else:
                    interval_counts = interval_counts.append({'Counts': high_intensity_count, 'Activation': False},
                                                             ignore_index=True)

            previous_high_intensity_counts = high_intensity_count
            i += 1

        self.interval_high_intensity_counts = interval_counts
