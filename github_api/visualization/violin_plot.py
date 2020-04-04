import matplotlib.pyplot as plt
import seaborn as sns

from .base_plot import BasePlot


class ViolinPlot(BasePlot):

    def __init__(self, args, df):
        self.args = args
        self.df = df
        self._set_changes_bins()

    def show(self):
        # FIXME: how to set both style and palette temporarily
        sns.set(style="whitegrid", palette="pastel", color_codes=True)
        sns.set(
            style=self.args.style,
            palette=self.args.palette,
            color_codes=True)

        figsize = (self.args.width, self.args.height)
        fig, ax = plt.subplots(2, 1, figsize=figsize)

        sns.violinplot(
            ax=ax[0],
            data=self.df,
            hue=self.hue_labels,
            inner=self.args.inner,
            x='changes_bins',
            y='elapsed_days')
        ax[0].axes.get_xaxis().set_visible(False)
        ax[0].legend(loc=self.args.loc)

        sns.violinplot(
            ax=ax[1],
            data=self.df,
            hue=self.hue_labels,
            inner=self.args.inner,
            x='changes_bins',
            y='elapsed_days_of_first_comment')
        ax[1].legend(loc=self.args.loc)

        sns.despine(fig=fig, right=True)


def create_changes_and_elapsed_days(args, df):
    vp = ViolinPlot(args, df)
    vp.show()
    plt.show()
