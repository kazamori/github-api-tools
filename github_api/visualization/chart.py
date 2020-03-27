import pandas as pd

from ..utils import log
from .scatter_plot import create_changes_and_elapsed_days


def output_chart(args, path):
    df = pd.read_csv(path)
    log.debug(f'DataFrame:\n{df}')
    create_changes_and_elapsed_days(args, df)
