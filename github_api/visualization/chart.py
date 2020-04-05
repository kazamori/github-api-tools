import pandas as pd

from ..utils import log


def output_chart(args, path):
    df = pd.read_csv(path)
    log.debug(f'DataFrame:\n{df}')
    args.plot.module.create_changes_and_elapsed_days(args, df)
