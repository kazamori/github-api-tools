import matplotlib.pyplot as plt
import seaborn as sns

from .base_plot import BasePlot


class ScatterPlot(BasePlot):

    def __init__(self, args, df):
        self.args = args
        self.df = df
        self._set_changes_bins()

    def show(self):
        col = self.args.col
        col_wrap = self.args.col_wrap

        if not self.has_labels():
            col = None
            col_wrap = None

        with sns.axes_style(self.args.style):
            sns.relplot(
                alpha=self.args.alpha,
                col=col,
                col_wrap=col_wrap,
                data=self.df,
                height=self.args.height,
                hue=self.hue_labels,
                kind='scatter',
                legend='full',
                palette=self.args.palette,
                size='changes_bins',
                sizes=self.changes_sizes,
                x='elapsed_days',
                y='elapsed_days_of_first_comment')
            plt.show()


def create_changes_and_elapsed_days(args, df):
    sp = ScatterPlot(args, df)
    sp.show()
    plt.show()
