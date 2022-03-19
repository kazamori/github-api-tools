import pandas as pd

from ...utils import log


def filter_dates(args, df):
    created_at = pd.to_datetime(df['created_at'])
    datefrom = args.datefrom <= created_at
    dateto = created_at <= args.dateto
    mask = datefrom & dateto
    filtered = created_at.loc[mask]
    return df[df.index.isin(filtered.index)]


def output_chart(args, path):
    df = pd.read_csv(path)
    if args.datefrom is not None and args.dateto is not None:
        df = filter_dates(args, df)
    log.debug(f'DataFrame:\n{df}')
    args.plot.module.create_changes_and_elapsed_days(args, df)
