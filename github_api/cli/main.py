import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path

from github import Github

from .. import cli
from ..consts import Plot
from ..core.repository import Repository
from ..core.writer import create_filename
from ..core.writer import output_csv
from ..utils import log
from ..utils import parse_datetime
from ..visualization.chart import output_chart
from .box_option import parse_box_argument
from .scatter_option import parse_scatter_argument
from .violin_option import parse_violin_argument


def has_plot_option(argv):
    for _, plot in Plot.__members__.items():
        if plot.value in argv:
            return True
    return False


def parse_dateto(s):
    return parse_datetime(s + ' 23:59:59')


def parse_datefrom(s):
    return parse_datetime(s + ' 00:00:00')


def parse_argument():
    parser = argparse.ArgumentParser()
    parser.set_defaults(
        datefrom=None,
        dateto=datetime.now(),
        enable_cache=True,
        exclude_commented_user=[],
        nop=False,
        _plot=Plot.SCATTER.value,
        plot=None,
        pr_id=None,
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
        '--exclude-commented-user', nargs='*', dest='exclude_commented_user',
        help='set user not to match first commented user e.g.) bot'
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
        '--pr-id', action='store', type=int, dest='pr_id',
        help='set arbitrary pull request number in given repository'
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

    # common seaborn parameters
    parser.add_argument(
        '--palette', action='store',
        help='set palette parameter for seaborn plot'
    )

    parser.add_argument(
        '--style', action='store',
        help='set style parameter for seaborn plot'
    )

    subparsers = parser.add_subparsers(dest='_plot')
    parse_box_argument(subparsers)
    parse_scatter_argument(subparsers)
    parse_violin_argument(subparsers)

    argv = sys.argv[1:]
    if not has_plot_option(argv):
        argv.extend(['--nop', Plot.SCATTER.value])

    args = parser.parse_args(argv)
    args.plot = Plot.from_str(args._plot)
    return args


def show_owner_repository(gh):
    me = gh.get_user()
    print(f'your account: {me.login}')
    print('your repositories:')
    for repo in gh.get_user().get_repos():
        if me.login == repo.owner.login:
            print(f' * {repo}')


def get_csv_path(args, repo_name, gh):
    filename = create_filename(repo_name)
    path = Path(filename)
    if args.enable_cache and path.exists():
        log.info(f'use existent {path}')
        return path

    with Repository(args, gh, repo_name) as repo:
        return output_csv(args, repo, filename)


def main():
    args = parse_argument()
    if args.verbose:
        log.setLevel(logging.DEBUG)
        log.debug(args)

    from .env import TOKEN

    gh = Github(TOKEN)

    if args.repositories is None:
        show_owner_repository(gh)
        return

    if args.user is None:
        args.user = gh.get_user().login

    if args.pr_id is not None:
        name = args.repositories[0]
        repo = Repository(args, gh, name)
        repo.get_pull(args.pr_id)
        return

    for name in args.repositories:
        path = get_csv_path(args, name, gh)
        output_chart(args, path)


if __name__ == '__main__':
    main()
