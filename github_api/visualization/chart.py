import pandas as pd

from . import box_plot
from . import scatter_plot
from ..consts import Plot
from ..utils import log


def output_chart(args, path):
    df = pd.read_csv(path)
    log.debug(f'DataFrame:\n{df}')

    if args.plot == Plot.BOX.value:
        box_plot.create_changes_and_elapsed_days(args, df)
    elif args.plot == Plot.SCATTER.value:
        scatter_plot.create_changes_and_elapsed_days(args, df)
    else:
        raise NotImplementedError(f'Unsupported plot: {args.plot}')
