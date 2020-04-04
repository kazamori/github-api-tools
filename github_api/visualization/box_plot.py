import matplotlib.pyplot as plt
import seaborn as sns

from .base_plot import BasePlot


class BoxPlot(BasePlot):

    def __init__(self, args, df):
        self.args = args
        self.df = df
        self._set_changes_bins()

    def show(self):
        # FIXME: how to set both style and palette temporarily
        sns.set(style=self.args.style, palette=self.args.palette)

        figsize = (self.args.width, self.args.height)
        fig, ax = plt.subplots(2, 1, figsize=figsize)
        ax[0].set_title(self.title)

        sns.boxplot(
            ax=ax[0],
            data=self.df,
            hue=self.hue_labels,
            x='changes_bins',
            y='elapsed_days')
        ax[0].axes.get_xaxis().set_visible(False)

        sns.boxplot(
            ax=ax[1],
            data=self.df,
            hue=self.hue_labels,
            x='changes_bins',
            y='elapsed_days_of_first_comment')

        sns.despine(fig=fig, offset=10, trim=True)


def create_changes_and_elapsed_days(args, df):
    bp = BoxPlot(args, df)
    bp.show()
    plt.show()
