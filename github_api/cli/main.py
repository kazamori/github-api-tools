import argparse
import logging
import sys
from pathlib import Path

from github import Github

from .. import cli
from ..consts import Plot
from ..core.repository import Repository
from ..core.writer import create_filename
from ..core.writer import output_csv
from ..utils import log
from ..visualization.chart import output_chart
from .box_option import parse_box_argument
from .scatter_option import parse_scatter_argument


def has_plot_option(argv):
    for _, plot in Plot.__members__.items():
        if plot.value in argv:
            return True
    return False


def parse_argument():
    parser = argparse.ArgumentParser()
    parser.set_defaults(
        enable_cache=True,
        nop=False,
        plot=Plot.SCATTER.value,
        repositories=[],
        verbose=False,
        version=cli.__version__,
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

    subparsers = parser.add_subparsers(dest='plot')
    parse_box_argument(subparsers)
    parse_scatter_argument(subparsers)

    argv = sys.argv[1:]
    if not has_plot_option(argv):
        argv.extend(['--nop', Plot.SCATTER.value])

    args = parser.parse_args(argv)
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

    with Repository(gh, repo_name) as repo:
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

    for name in args.repositories:
        path = get_csv_path(args, name, gh)
        output_chart(args, path)


if __name__ == '__main__':
    main()
