import seaborn as sns
import pandas as pd
from pathlib import Path
import plotly.express as px
from Shared.Classes.Cell import Cell
from CLI.RuntimeConstants.Runtime_Datasets import TimeFrameColumns


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
    def plot_true_signal_pie_chart(folder: Path, file_name: str, cells: list):
        # True Signal is defined as a cell having more than 50% of true signals for each timeframe
        df = pd.DataFrame(columns=['Cell', 'True Signal'])
        cell: Cell
        for cell in cells:
            df = df.append(cell.normalized_time_frames)
            df['Cell'].fillna(cell.name, inplace=True)
            if (cell.normalized_time_frames[f'{TimeFrameColumns.TRUE_SIGNAL.value}'].value_counts(
                    normalize=True))[1] > 0.5:
                exclude = False
            else:
                exclude = True

            df['True Signal'].fillna(exclude, inplace=True)

            if exclude:
                df['True Signal'].fillna('Active', inplace=True)
            else:
                df['True Signal'].fillna('Inactive', inplace=True)

        df = df.drop_duplicates(subset=['Cell'])
        df.drop(['Spike', 'Value', 'Including Minute'], axis=1, inplace=True)
        df["True Signal Int"] = df["True Signal"].astype(int)
        df = df.reset_index()
        del df['index']
        df.replace({"True Signal": {True: "Active", False: "Inactive"}}, inplace=True)

        df['True Signal Int'] = 1

        fig = px.pie(df, values='True Signal Int', names='True Signal',
                     title="Percentage of active and inactive cells")

        fig.write_html(
            str(Path.joinpath(folder, f"{file_name}_active_cells.html")))
        fig.write_image(str(
            Path.joinpath(folder, f"{file_name}_file_active_cells.png")))
