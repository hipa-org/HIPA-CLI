from CLI.RuntimeConstants import Runtime_Datasets
import pandas as pd
from Shared.Classes.File import File
from Shared.Classes.Cell import Cell


class DataHandler:

    @staticmethod
    def generate_merged_time_frame_df():
        """
        Merges all timeframe data together from all files
        """
        df = pd.DataFrame(columns=['file', 'cell'])

        file: File
        cell: Cell
        for file in Runtime_Datasets.Files:
            for cell in file.cells:
                df = df.append(cell.normalized_time_frames)
                df['cell'].fillna(cell.name, inplace=True)
                df['file'].fillna(file.name, inplace=True)

        return df
