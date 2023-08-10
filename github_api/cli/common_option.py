import argparse
from datetime import datetime
from pathlib import Path

import pytz

from .. import cli
from ..core.repository import Repository
from ..utils import create_filename
from ..utils import log
from ..utils import output_csv
from ..utils import parse_datetime


def parse_dateto(s):
    return parse_datetime(s + ' 23:59:59')


def parse_datefrom(s):
    return parse_datetime(s + ' 00:00:00')


def get_common_parser():
    parser = argparse.ArgumentParser()
    parser.set_defaults(
        datefrom=None,
        dateto=pytz.UTC.localize(datetime.now()),
        enable_cache=True,
        nop=False,
        repositories=[],
        user=None,
        verbose=False,
        version=cli.__version__,
    )

    parser.add_argument(
        '--from', action='store', dest='datefrom', type=parse_datefrom,
        help='filter created_at FROM: e.g. 2020-04-06'
    )

    parser.add_argument(
        '--to', action='store', dest='dateto', type=parse_dateto,
        help='filter created_at TO: e.g. 2020-04-06'
    )

    parser.add_argument(
        '--disable-cache', action='store_false', dest='enable_cache',
        help='disable cache'
    )

    parser.add_argument(
        '--nop', action='store_true',
        help='use as a separator for option handling of positional argument'
    )

    parser.add_argument(
        '--repository', nargs='*', dest='repositories',
        help='set repositories'
    )

    parser.add_argument(
        '--user', action='store',
        help='set user to filter assignee of pull request'
    )

    parser.add_argument(
        '--verbose', action='store_true',
        help='set verbose mode'
    )

    parser.add_argument(
        '--version', action='version', version=f'%(prog)s {cli.__version__}',
        help='show version'
    )

    return parser


def get_csv_path(args, repo_name, gh, create_data):
    filename = create_filename(repo_name, args.api)
    path = Path(filename)
    if args.enable_cache and path.exists():
        log.info(f'use existent {path}')
        return path

    with Repository(args, gh, repo_name) as repo:
        data = create_data(repo)
        return output_csv(args, data, filename)
