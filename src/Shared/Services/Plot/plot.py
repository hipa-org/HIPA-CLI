import seaborn as sns
import pandas as pd
from pathlib import Path


class PlotService:
    @staticmethod
    def plot_peaks_per_minute(peaks_per_minutes, folder):
        df = pd.DataFrame(columns=['peaks'])
        df['peaks'] = pd.Series(peaks_per_minutes)
        df.reset_index(inplace=True)
        df = df.rename(columns={'index': 'minutes'})
        print(df)
        ax = sns.barplot(x="minutes", y="peaks", data=df)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90, horizontalalignment='right')
        fig = ax.get_figure()
        fig.savefig(Path.joinpath(folder, "plots_per_minutes.png"), bbox_inches='tight')


    @staticmethod
    def plot_peaks_per_minute_per_cell(peaks_per_minutes_per_cell, folder):
        df = pd.DataFrame(columns=['peaks'])
        print(peaks_per_minutes_per_cell)
